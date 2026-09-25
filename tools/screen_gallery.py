"""Progressively enhanced product screen decks; no fabricated product interfaces."""
from html import escape as e

def preview_screens(project):
 if project.get('previewMode')=='single': return []
 screens=project.get('screens',[])
 # Keep curated order and deduplicate the same source image.
 seen=set();result=[]
 for screen in screens:
  if screen['src'] not in seen:
   seen.add(screen['src']);result.append(screen)
 return result

def screen_gallery(project,layered=False):
 screens=preview_screens(project)
 portrait=all(s['height']>s['width']*1.4 for s in screens)
 cls='screen-gallery'+(' is-layered' if layered else '')+(' is-portrait' if portrait else '')
 out=f'<div class="{cls}" data-screen-gallery aria-label="{e(project["name"])} product screens"><div class="screen-stage">'
 for i,s in enumerate(screens):
  state='is-front' if i==0 else 'is-back' if i==1 else 'is-third' if i==2 and portrait else ''
  out+=f'<a class="screen-shot {state}" href="{project["id"]}.html" aria-label="Explore {e(project["name"])}: {e(s["alt"])}"'+(' tabindex="-1" aria-hidden="true"' if i else '')+f'><img src="{e(s["src"])}" alt="{e(s["alt"])}" width="{s["width"]}" height="{s["height"]}" loading="lazy"></a>'
 out+='</div><div class="screen-controls" hidden><div class="screen-options" role="group" aria-label="Choose a product screen">'
 for i,s in enumerate(screens):
  out+=f'<button type="button" data-screen-index="{i}" data-caption="{e(s["caption"])}" aria-label="Show {e(s["alt"])}" aria-pressed="{str(i==0).lower()}" title="{e(s.get("label",s["alt"]))}"><img src="{e(s["src"])}" alt="" width="{s["width"]}" height="{s["height"]}" loading="lazy"></button>'
 out+=f'</div><span class="screen-count" aria-live="polite">1 / {len(screens)}</span></div>'
 if layered: out+=f'<p class="featured-caption screen-caption">{e(screens[0]["caption"])}</p>'
 return out+'</div>'
