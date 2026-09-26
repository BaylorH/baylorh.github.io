// Optional first-party configuration. No network request until a visitor opts in.
(() => {
  const id=document.querySelector('meta[name="analytics-id"]')?.content || '';
  if (!/^G-[A-Z0-9]+$/.test(id) || !['baylor-harrison.com','www.baylor-harrison.com'].includes(location.hostname)) return;
  const key='portfolio-analytics-choice-v1';
  let enabled=false,loaded=false;
  let choice;
  try { choice=localStorage.getItem(key); } catch { choice=null; }
  let referrer='';
  try { if(document.referrer) { const url=new URL(document.referrer); referrer=url.origin; } } catch {}
  function emit(){window.dataLayer=window.dataLayer||[];window.dataLayer.push(arguments);}
  function start(){
    enabled=true;window[`ga-disable-${id}`]=false;
    if(loaded)return;
    loaded=true;
    emit('js',new Date());
    emit('config',id,{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:location.origin+location.pathname,page_referrer:referrer});
    emit('event','page_view',{page_title:document.title,page_location:location.origin+location.pathname,page_referrer:referrer});
    const script=document.createElement('script');script.async=true;script.src=`https://www.googletagmanager.com/gtag/js?id=${id}`;document.head.append(script);
  }
  const panel=document.createElement('section');panel.className='analytics-choice';panel.setAttribute('aria-label','Optional visitor analytics');
  const text=document.createElement('p');text.textContent='Allow basic visitor analytics? This helps improve the portfolio by measuring visits and link clicks.';
  const allow=document.createElement('button');allow.type='button';allow.textContent='Allow analytics';
  const decline=document.createElement('button');decline.type='button';decline.textContent='No thanks';
  const settings=document.createElement('button');settings.type='button';settings.className='analytics-settings';settings.textContent='Analytics settings';
  function save(value){
    choice=value;
    try{localStorage.setItem(key,value);}catch{}
    if(value==='granted')start();
    else{enabled=false;window[`ga-disable-${id}`]=true;}
    panel.hidden=true;
  }
  allow.addEventListener('click',()=>save('granted'));
  decline.addEventListener('click',()=>save('denied'));
  settings.addEventListener('click',()=>{panel.hidden=false;});
  panel.append(text,allow,decline);panel.hidden=choice==='granted'||choice==='denied';
  document.body.append(panel,settings);
  if(choice==='granted')start();
  document.addEventListener('click',event=>{
    if(!enabled)return;
    const link=event.target.closest('a[href]');if(!link)return;
    const href=link.getAttribute('href');
    if(href.startsWith('mailto:'))emit('event','contact_click',{contact_method:'email'});
    else if(href.startsWith('tel:'))emit('event','contact_click',{contact_method:'phone'});
    else if(/\.pdf(?:$|[?#])/.test(href))emit('event','document_click',{document_name:href.split('/').pop().split(/[?#]/)[0]});
    else {
      const url=new URL(href,location.href);
      if(url.origin===location.origin&&/^\/(?!resume\/)[a-z0-9-]+\/$/.test(url.pathname))emit('event','project_open',{page_path:url.pathname});
    }
  });
})();
