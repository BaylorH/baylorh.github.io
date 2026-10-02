"""The mark shown beside each "Built with" tag on a product page. The six colour marks are the home page's own."""
from html import escape as e
T='technology/';S='stack/'
ICONS={
 # Named technologies
 'React':T+'react','TypeScript':T+'typescript','Node.js':T+'nodejs','Swift':T+'swift',
 'Python':T+'python','Python pipeline':T+'python','Python CLI':T+'python',
 'Firebase':T+'firebase','Firebase Auth':T+'firebase','Firestore':T+'firebase',
 'JavaScript':S+'javascript','Preact':S+'preact','Tailwind CSS':S+'tailwind','Three.js':S+'threejs','Unity':S+'unity','C#':S+'csharp','Java':S+'coffee',
 'Google Cloud':S+'googlecloud','Google Cloud Run':S+'googlecloud','Google Sheets':S+'googlesheets','Chrome extension':S+'chrome','Gemini image models':S+'gemini',
 'AWS':S+'aws','AWS Lambda':S+'aws','DynamoDB':S+'aws','Amazon SES':S+'aws',
 'Shopify':S+'shopify','Shopify theme':S+'shopify','Shopify Admin API':S+'shopify','Asana API':S+'asana',
 'OpenAI API':S+'openai','ChatGPT connector':S+'openai',
 # Capabilities
 'AI APIs':S+'sparkles','LLM APIs':S+'sparkles','LLM API':S+'sparkles','Machine learning':S+'brain-circuit',
 'AI computer-use agent':S+'mouse-pointer-click','AI-assisted extraction':S+'scan-text','LLM extraction':S+'scan-text','LLM routing':S+'route','Retrieval':S+'file-search','Vision model':S+'scan-eye','Voice':S+'mic',
 'APIs':S+'plug','Content-system APIs':S+'plug','Agent connections':S+'network','Cloud services':S+'cloud','Cloud applications':S+'cloud',
 'Dashboard':S+'layout-dashboard','Dashboards':S+'layout-dashboard','Data visualization':S+'chart-column','Graph visualization':S+'waypoints','Knowledge graphs':S+'waypoints',
 'Search':S+'search','Email automation':S+'mail-check','Spreadsheet parsing':S+'sheet','Data matching':S+'git-compare-arrows','Verification':S+'badge-check',
 'Project management':S+'list-checks','Delivery coordination':S+'users','Organization roles':S+'users',
 'Headless browser':S+'app-window','Headless simulation':S+'cpu','Rapier physics':S+'atom','State machines':S+'workflow','Game systems':S+'gamepad-2',
 '3D visualization':S+'box','3D environments':S+'mountain','Animation':S+'clapperboard','Maps':S+'map','Location services':S+'map-pin',
}

def chip(label):
 # A missing entry is a build error on purpose: a tag never appears without its mark.
 return f'<span><img src="images/{ICONS[label]}.svg" alt="" width="18" height="18" loading="lazy">{e(label)}</span>'
