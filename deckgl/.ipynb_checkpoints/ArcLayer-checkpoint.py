from IPython.core.display import HTML, display
import json

import templates

class Base(object):

    def __init__(self, data, access_token=None):
        
        self.access_token = access_token
        if access_token is None:
            self.access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
            
        self.data = data
        
        self.div_id = 'map'
        self.width = '100%'
        self.height = '500px'
        self.template = 'ArcLayer'

class ArcLayer(Base):
    """Create ArcLayer"""
    
    def __init__(self, data, access_token=None):
        super(ArcLayer, self).__init__(data, access_token)
    
    def create_html(self, filename=None):
        options = dict(
            accessToken=self.access_token,
            data=json.dumps(self.data, ensure_ascii=False)
        )
        return templates.format(self.template, **options)
    
    def as_iframe(self, html_data):
        """Build the HTML representation for the mapviz."""

        srcdoc = html_data.replace('"', "'")
        return ('<iframe id="{div_id}", srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height};"></iframe>'.format(
                    div_id=self.div_id,
                    srcdoc=srcdoc,
                    width=self.width,
                    height=self.height))

    def show(self):
        # Load the HTML iframe
        html = self.create_html()
        map_html = self.as_iframe(html)

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))

    