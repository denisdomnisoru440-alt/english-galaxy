import re

path = r'C:\Users\denis\OneDrive\Рабочий стол\english-galaxy\vocab.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove Dota data
lines = html.split('\n')
new_lines = []
for line in lines:
    if 'var g6 = JSON.parse' in line and 'Dota2_English' in line:
        continue
    if line.strip() == 'G.push(g6);':
        continue
    if 'var g7 = JSON.parse' in line and 'Gaming_Dota2' in line:
        continue
    if line.strip() == 'G.push(g7);':
        continue
    new_lines.append(line)
html = '\n'.join(new_lines)

# 2. Remove Dota from CC
html = html.replace('"Gaming_Dota2":"#f472b6","Dota2_English":"#ec4899",', '')

# 3. Replace page divs
old_pages = '<div class="page" id="history"></div>\n<div class="page" id="random"></div>\n<div class="page" id="mywords"></div>\n<div class="page" id="notes"></div>'
html = html.replace(old_pages, '<div class="page" id="me"></div>')

# 4. Replace nav
old_nav = """<a data-tab="history" onclick="switchTab('history')"><span class="ic">&#128202;</span>History</a>
<a data-tab="random" onclick="switchTab('random')"><span class="ic">&#127922;</span>Random</a>
<a data-tab="mywords" onclick="switchTab('mywords')"><span class="ic">&#128221;</span>My Words</a>
<a data-tab="notes" onclick="switchTab('notes')"><span class="ic">&#128221;</span>Notes</a>"""
html = html.replace(old_nav, '<a data-tab="me" onclick="switchTab(\'me\')"><span class="ic">&#128100;</span>Me</a>')

# 5. Replace switchTab function - find and replace
old_switch_end = """   else if(tab=='history')renderHistory();
   else if(tab=='random')renderRandom();
   else if(tab=='mywords')renderMyWords();
   else if(tab=='notes')renderNotes();
}"""

new_stuff = """   else if(tab=='me')renderMe();
}
var meSub=null;
var ME_T='meInner';
function openMeSub(s){meSub=s;renderMe();}
function renderMe(){
  var d=document.getElementById('me');
  if(!meSub){
    var h='<div style="font-size:13px;font-weight:700;color:#8c93b8;margin-bottom:10px">&#128100; Me</div>';
    h+='<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">';
    h+='<div onclick="openMeSub(\'stats\')" style="background:linear-gradient(135deg,#6366f1,#818cf8);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#128200;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">Stats</div></div>';
    h+='<div onclick="openMeSub(\'history\')" style="background:linear-gradient(135deg,#ef4444,#f97316);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#128202;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">History</div></div>';
    h+='<div onclick="openMeSub(\'mywords\')" style="background:linear-gradient(135deg,#22c55e,#10b981);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#128156;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">My Words</div></div>';
    h+='<div onclick="openMeSub(\'random\')" style="background:linear-gradient(135deg,#f97316,#eab308);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#127922;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">Random</div></div>';
    h+='<div onclick="openMeSub(\'notes\')" style="background:linear-gradient(135deg,#7c5cfc,#a78bfa);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#128221;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">Notes</div></div>';
    h+='<div onclick="openMeSub(\'sync\')" style="background:linear-gradient(135deg,#06b6d4,#22d3ee);border-radius:12px;padding:16px;text-align:center;cursor:pointer;touch-action:manipulation"><div style="font-size:24px">&#128260;</div><div style="color:#fff;font-size:12px;font-weight:700;margin-top:4px">Sync</div></div>';
    h+='</div>';
    d.innerHTML=h;return;
  }
  d.innerHTML='<div onclick="openMeSub(null)" style="color:#7c5cfc;font-size:11px;margin-bottom:10px;cursor:pointer">&#8592; Back</div><div id="meInner"></div>';
  if(meSub=='stats')renderStatsTo('meInner');
  else if(meSub=='history')renderHistoryTo('meInner');
  else if(meSub=='mywords')renderMyWordsTo('meInner');
  else if(meSub=='random')renderRandomTo('meInner');
  else if(meSub=='notes')renderNotesTo('meInner');
  else if(meSub=='sync')renderSyncTo('meInner');
}
function renderHistoryTo(t){ME_T=t;renderHistory();}
function renderStatsTo(t){ME_T=t;renderStats();}
function renderMyWordsTo(t){ME_T=t;renderMyWords();}
function renderRandomTo(t){ME_T=t;renderRandom();}
function renderNotesTo(t){ME_T=t;renderNotes();}"""

html = html.replace(old_switch_end, new_stuff)

# 6. Add renderSyncTo before the end of script
sync_func = """
function renderSyncTo(t){
  var el=document.getElementById(t);
  var keys=['eg_known','eg_study_words','eg_quiz_history','eg_grammar_history','eg_scores','eg_daily_stats','eg_notes'];
  var total=0;
  for(var i=0;i<keys.length;i++){var v=lsGet(keys[i]);if(v)total+=v.length;}
  var kb=(total/1024).toFixed(1);
  var h='<div style="font-size:13px;font-weight:700;color:#06b6d4;margin-bottom:8px">&#128260; Data Sync</div>';
  h+='<div style="background:#11162e;border-radius:12px;padding:14px;margin-bottom:10px">';
  h+='<div style="color:#8c93b8;font-size:11px;margin-bottom:8px">Export all your data to a file, then import on another device.</div>';
  h+='<div style="color:#5a6190;font-size:10px">Data size: '+kb+' KB</div></div>';
  h+='<div style="display:flex;gap:8px;margin-bottom:10px">';
  h+='<button onclick="exportData()" style="flex:1;background:linear-gradient(135deg,#06b6d4,#10b981);border:none;border-radius:12px;color:#fff;font-size:13px;font-weight:700;padding:12px;cursor:pointer;touch-action:manipulation">&#128228; Export</button>';
  h+='<button onclick="document.getElementById(\\'importFile\\').click()" style="flex:1;background:linear-gradient(135deg,#f97316,#ef4444);border:none;border-radius:12px;color:#fff;font-size:13px;font-weight:700;padding:12px;cursor:pointer;touch-action:manipulation">&#128229; Import</button>';
  h+='</div>';
  h+='<input type="file" id="importFile" accept=".json" style="display:none" onchange="importData(event)">';
  h+='<div id="syncStatus" style="color:#8c93b8;font-size:10px;text-align:center;margin-top:6px"></div>';
  h+='<div style="background:#11162e;border-radius:12px;padding:14px;margin-top:10px">';
  h+='<div style="color:#7c5cfc;font-size:11px;font-weight:700;margin-bottom:6px">&#128161; How to sync:</div>';
  h+='<div style="color:#5a6190;font-size:10px;line-height:1.6">1. Export on device A<br>2. Send file to device B<br>3. Import on device B<br>4. All data appears!</div></div>';
  el.innerHTML=h;
}
function exportData(){
  var keys=['eg_known','eg_study_words','eg_quiz_history','eg_grammar_history','eg_scores','eg_daily_stats','eg_notes','eg_theme','eg_theme_man'];
  var data={version:1,exported:new Date().toISOString(),data:{}};
  for(var i=0;i<keys.length;i++){var v=lsGet(keys[i]);if(v)data.data[keys[i]]=v;}
  var json=JSON.stringify(data);
  var blob=new Blob([json],{type:'application/json'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');
  a.href=url;a.download='english-galaxy-backup-'+new Date().toISOString().slice(0,10)+'.json';
  document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);
  var s=document.getElementById('syncStatus');if(s)s.innerHTML='<span style="color:#10b981">&#10004; Exported!</span>';
}
function importData(e){
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){
    try{
      var data=JSON.parse(ev.target.result);
      if(!data||!data.data){var s=document.getElementById('syncStatus');if(s)s.innerHTML='<span style="color:#ef4444">&#10060; Invalid file</span>';return;}
      var count=0;var keys=Object.keys(data.data);
      for(var i=0;i<keys.length;i++){lsSet(keys[i],data.data[keys[i]]);count++;}
      var dt=new Date(data.exported);
      var s=document.getElementById('syncStatus');if(s)s.innerHTML='<span style="color:#10b981">&#10004; Imported! '+count+' keys</span>';
      setTimeout(function(){location.reload();},1200);
    }catch(ex){
      var s=document.getElementById('syncStatus');if(s)s.innerHTML='<span style="color:#ef4444">&#10060; Error</span>';
    }
  };
  reader.readAsText(file);e.target.value='';
}
"""
html = html.replace('renderBrowse();', sync_func + '\nrenderBrowse();')

# 7. Fix renderHistory target
html = html.replace("document.getElementById('history').innerHTML=h;\n  renderStats();showReview();", "document.getElementById(ME_T).innerHTML=h;")

# 8. Fix renderRandom target
html = html.replace("document.getElementById('random').innerHTML=h;", "document.getElementById(ME_T).innerHTML=h;")

# 9. Fix renderMyWords targets
html = html.replace("document.getElementById('mywords')", "document.getElementById(ME_T)")

# 10. Fix renderNotes targets
html = html.replace("document.getElementById('notes')", "document.getElementById(ME_T)")

# 11. Fix renderStats targets
html = html.replace("document.getElementById('statsTab')", "document.getElementById(ME_T)")

# 12. Fix toggleBMK
html = html.replace("if(mode=='mywords')renderMyWords();", "if(mode=='me'&&meSub=='mywords')renderMyWords();")

# 13. Remove switchHTab
shtab = """function switchHTab(i){
  document.getElementById(ME_T).style.display=i===0?'block':'none';
  document.getElementById(ME_T).style.display=i===1?'block':'none';
  document.getElementById(ME_T).style.display=i===2?'block':'none';
  var btns=document.querySelectorAll('.sttab button');
  for(var b=0;b<btns.length;b++)btns[b].classList.toggle('act',b===i);
}"""
html = html.replace(shtab, '')

# Also try the original
shtab2 = """function switchHTab(i){
  document.getElementById('statsTab').style.display=i===0?'block':'none';
  document.getElementById('reviewTab').style.display=i===1?'block':'none';
  document.getElementById('histList').style.display=i===2?'block':'none';
  var btns=document.querySelectorAll('.sttab button');
  for(var b=0;b<btns.length;b++)btns[b].classList.toggle('act',b===i);
}"""
html = html.replace(shtab2, '')

# Verify
bt = html.count('`')
print(f"Backticks: {bt} (even: {bt % 2 == 0})")
print(f"Dota removed: {'Dota2_English' not in html and 'Gaming_Dota2' not in html}")
print(f"Has me page: {'id=\"me\"' in html}")
print(f"Has renderMe: {'function renderMe' in html}")
print(f"Has renderSyncTo: {'function renderSyncTo' in html}")
print(f"Tab count: {html.count('data-tab=')}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("DONE")
