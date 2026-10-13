"""Read declared fixture notation; no utterance interpretation or business rules."""
import numbers
import re


def equal(a,b):
    if isinstance(a,bool) != isinstance(b,bool):return False
    return a==b


def target_notation(value):
    if not isinstance(value,dict) or 'question_id' not in value:return None
    if value.get('whole_question'):return {value['question_id'],value['question_id']+'.*'}
    if 'slot_id' not in value:return None
    repeat=('#'+value['repeat_key']) if value.get('repeat_key') else ''
    return {value['question_id']+repeat+'.'+value['slot_id']}


def value_preserved(source,wire,node,definition,pointer,source_pointer,defs,notation):
    if equal(source,wire):return True
    vocab=notation['vocabularies'];conventions=notation['representation_conventions']
    families=[definition+pointer,definition]
    if '$ref' in node:families.insert(0,node['$ref'].split('/')[-1])
    families +=[b['$ref'].split('/')[-1] for op in ('oneOf','anyOf') for b in node.get(op,[]) if '$ref' in b]
    if isinstance(source,str):
        for family in families:
            mapping=vocab.get(family,{})
            if source in mapping and equal(mapping[source],wire):return True
        mapping=conventions['field_values'].get(definition+pointer,{})
        if source in mapping and equal(mapping[source],wire):return True
    key=source_pointer.split('/')[-1].replace('~1','/').replace('~0','~')
    if pointer.endswith('/kind') and key in conventions['discriminator_keys']:
        if equal(conventions['discriminator_keys'][key],wire):return True
    if isinstance(source,str) and source in conventions['nullable_tokens'] and wire is None:
        return any(b.get('type')=='null' for op in ('anyOf','oneOf') for b in node.get(op,[]))
    if isinstance(source,numbers.Real) and not isinstance(source,bool) and wire==str(source):return True
    if isinstance(wire,dict):
        notation_values=target_notation(wire)
        if notation_values is not None and isinstance(source,str) and source in notation_values:return True
        if set(wire)=={'answer'}:
            return value_preserved(source,wire['answer'],defs['Value'],'Value','',source_pointer,defs,notation)
        if set(wire)=={'amount','unit'}:
            if isinstance(source,numbers.Real) and not isinstance(source,bool):return equal(source,wire['amount'])
            if isinstance(source,str):
                amount=format(wire['amount'],'g');unit=wire['unit']
                rendered=unit.replace('n',amount) if 'n' in unit else amount+unit
                return re.sub(r'\s+','',source)==re.sub(r'\s+','',rendered)
        if set(wire)=={'handled'}:return equal(source,wire['handled'])
    if isinstance(wire,list):
        if not isinstance(source,(list,dict)) and len(wire)==1:
            return value_preserved(source,wire[0],{},definition,pointer,source_pointer,defs,notation)
        if isinstance(source,list) and len(source)==len(wire):
            return all(value_preserved(a,b,{},definition,pointer,source_pointer,defs,notation) for a,b in zip(source,wire))
        if isinstance(source,dict) and len(source)==len(wire):
            # Named count maps are encoded as subject/question/slot + count rows.
            if all(isinstance(row,dict) and 'count' in row for row in wire):
                remaining=list(wire)
                for subject,count in source.items():
                    match=None
                    for i,row in enumerate(remaining):
                        identity=row.get('question_id',row.get('slot',row.get('subject')))
                        identities=target_notation(identity) if isinstance(identity,dict) else {identity}
                        if isinstance(identity,dict) and 'untargeted' in identity:
                            aliases=vocab['AskSubject/oneOf/1/properties/untargeted']
                            identities={k for k,v in aliases.items() if v==identity['untargeted']}
                        if subject in (identities or set()) and equal(count,row['count']):match=i;break
                    if match is None:return False
                    remaining.pop(match)
                return True
    return False
