import data from './data.js';

export class Explorer {
  tab = $state('map');
  component = $state('');
  type = $state('ParserOutput');
  caseId = $state('B1');
  specimen = $state('');
  edge = $state('');
  query = $state('');
  typeScope = $state('boundary');
  dark = $state(false);

  go(tab, value) {
    this.tab = tab;
    if (tab === 'contracts' && value) { this.type = value; this.typeScope = 'all'; }
    if (tab === 'cases' && value) { this.caseId = value; this.specimen = ''; }
    if (tab === 'map' && value) { this.component = value; this.edge = ''; }
    this.query = '';
    this.sync(true);
  }
  sync(push = false) {
    const value = this.tab === 'contracts' ? this.type : this.tab === 'cases' ? this.caseId : this.component;
    history[push ? 'pushState' : 'replaceState'](null, '', '#view=' + this.tab + '&item=' + encodeURIComponent(value));
  }
  restore() {
    const p = new URLSearchParams(location.hash.slice(1));
    const requested = p.get('view'), item = p.get('item');
    const tab = requested === 'pending' ? 'proposals' : requested;
    if (!['map', 'contracts', 'cases', 'proposals'].includes(tab)) return;
    this.tab = tab;
    if (tab === 'contracts' && data.definitions[item]) { this.type = item; this.typeScope = 'all'; }
    if (tab === 'cases' && data.cases.some(c => c.id === item)) this.caseId = item;
    if (tab === 'map' && !item) { this.component = ''; this.edge = ''; }
    if (tab === 'map' && data.components.some(c => c.id === item)) this.component = item;
  }
}
