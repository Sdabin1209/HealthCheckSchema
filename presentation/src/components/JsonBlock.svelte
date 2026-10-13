<script>
  import { json, download } from '../lib/data.js';
  let { value, label = 'JSON', filename = 'example.json' } = $props();
</script>
<div class="json-block">
  <div class="json-header"><span>{label}</span><button class="quiet" onclick={() => download(filename, value)}>JSON 저장 ↓</button></div>
  <div class="json-content" tabindex="0" role="textbox" aria-readonly="true" aria-multiline="true" aria-label={label}><pre>{json(value)}</pre></div>
</div>
