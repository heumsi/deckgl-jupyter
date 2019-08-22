import os
import json

from IPython.core.display import HTML, display

import templates
from mapboxgl.viz import MapViz
from mapboxgl.utils import *

MAX_SAFE_INTEGER = 9007199254740991

class Map(MapViz):

    def __init__(self, 
                 data=None, 
                 id='Map',
                 pickable=False,
                 onHover=None,
                 onClick=None,
                 visible=True,
                 opacity=1,
                 frame_width = '100%',
                 frame_height = '500px',
                 *args, **kwargs):
        super(Map, self).__init__(data, *args, **kwargs)
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.template = 'map'
        self.defaultProps = {}

        self.data = data
        self.id = id
        self.visible = visible
        self.opacity = opacity
        self.pickable = pickable
        self.onHover = onHover
        self.onClick = onClick
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def get_options(self):
        return dict(
            # Mapbox options.
            accessToken=self.access_token,
            div_id=self.div_id,
            style=self.style,
            center=list(self.center),
            zoom=self.zoom,
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            belowLayer=self.below_layer,
            opacity=self.opacity,
            minzoom=self.min_zoom,
            maxzoom=self.max_zoom,
            pitch=self.pitch, 
            bearing=self.bearing,
            boxZoomOn=self.box_zoom_on,
            doubleClickZoomOn=self.double_click_zoom_on,
            scrollZoomOn=self.scroll_zoom_on,
            touchZoomOn=self.touch_zoom_on,
            popupOpensOnHover=self.popup_open_action=='hover',
            includeSnapshotLinks=self.add_snapshot_links,
            preserveDrawingBuffer=self.add_snapshot_links,
            showScale=self.scale,
            scaleUnits=self.scale_unit_system,
            scaleBorderColor=self.scale_border_color,
            scalePosition=self.scale_position,
            scaleFillColor=self.scale_background_color,
            scaleTextColor=self.scale_text_color,

            # DeckGL options.
            data = self.data,
            id = self.id,
            visible = self.visible,
            pickable = self.pickable,
            onHover = self.onHover,
            onClick = self.onClick,
        )
    
    def as_iframe(self, html_data):
        srcdoc = html_data.replace('"', "'")
        return ('<iframe id="{div_id}", srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height};"></iframe>'.format(
                    div_id=self.div_id,
                    srcdoc=srcdoc,
                    width=self.frame_width,
                    height=self.frame_height
                ))

    def make_str(self, options):
        for k, v in options.items():
            if isinstance(v, str):
                options[k] = "'{}'".format(v)
            elif isinstance(v, bool):
                options[k] = json.dumps(v)
        return options

    def create_html(self, filename=None):

        # Create layer html
        layer_html = ''
        for layer in self.layers:
            options = layer.get_options()
            options = self.make_str(options)
            html = templates.format(layer.template, **options)
            layer_html += html + ','

        # Create base html
        options = self.get_options()
        options = self.make_str(options)
        options['layers'] = layer_html

        html = templates.format(self.template, **options)
        return html

    def show(self, **kwargs):
        # Load the HTML iframe
        html = self.create_html(**kwargs)
        map_html = self.as_iframe(html)

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))


class ArcLayer(Map):
    
    def __init__(self, 
                 data,
                 id='ArcLayer',
                 source_color=[0, 0, 0, 255],
                 target_color=[0, 0, 0, 255],
                 width=1,
                 widthUnits='pixels',
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 height=1,
                 tilt=0,
                 *args, 
                 **kwargs):
        super(ArcLayer, self).__init__(data, id, *args, **kwargs)

        self.template = 'ArcLayer'
        self.source_color = source_color
        self.target_color = target_color
        self.width = width
        self.widthUnits = widthUnits
        self.widthScale = widthScale
        self.widthMinPixels = widthMinPixels
        self.widthMaxPixels = widthMaxPixels
        self.height = height
        self.tilt = tilt

    def get_options(self):
        return dict(
            data=self.data,
            id=self.id,
            source_color=self.source_color,
            target_color=self.target_color,
            width=self.width,
            widthUnits=self.widthUnits,
            widthScale=self.widthScale,
            widthMinPixels=self.widthMinPixels,
            widthMaxPixels=self.widthMaxPixels,
            height=self.height,
            tilt=self.tilt
        )  

class PathLayer(Map):
    
    def __init__(self, 
                 data,
                 id='PathLayer',
                 width=1,
                 widthUnits=1,
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 rounded=False,
                 billboard=False,
                 miterLimit=4,
                 dashJustified=False,
                 tooltip='object.name',
                 *args, 
                 **kwargs):
        super(PathLayer, self).__init__(data, id, *args, **kwargs)

        self.template = 'PathLayer'
        self.width = width
        self.widthUnits = widthUnits
        self.widthScale = widthScale
        self.widthMinPixels = widthMinPixels
        self.widthMaxPixels = widthMaxPixels
        self.rounded = rounded
        self.billboard = billboard
        self.miterLimit = miterLimit
        self.dashJustified = dashJustified
        self.tooltip = tooltip

    def get_options(self):
        return dict(
            data=self.data,
            id=self.id,
            width=self.width,
            widthUnits=self.widthUnits,
            widthScale=self.widthScale,
            widthMinPixels=self.widthMinPixels,
            widthMaxPixels=self.widthMaxPixels,
            rounded=self.rounded,
            billboard=self.billboard,
            miterLimit=self.miterLimit,
            dashJustified=self.dashJustified,
            tooltip=self.tooltip
        )

class TripsLayer(PathLayer):
    
    def __init__(self, 
                 data,
                 id='TripsLayer',
                 currentTime=0,
                 trailLength=120,
                 width=1,
                 widthUnits=1,
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 rounded=False,
                 billboard=False,
                 miterLimit=4,
                 dashJustified=False,
                 tooltip='object.name',
                 *args, 
                 **kwargs):
        super(TripsLayer, self).__init__(data, 
                                        id=id,
                                        width=width,
                                        widthUnits=widthUnits,
                                        widthScale=widthScale,
                                        widthMinPixels=widthMinPixels,
                                        widthMaxPixels=widthMaxPixels,
                                        rounded=rounded,
                                        billboard=billboard,
                                        miterLimit=miterLimit,
                                        dashJustified=dashJustified,
                                        *args, **kwargs)

        self.template = 'TripsLayer'
        self.currentTime = currentTime
        self.trailLength = trailLength

    def get_options(self):
        options = super().get_options()
        options.update(
            currentTime = self.currentTime,
            trailLength = self.trailLength
        )
        return options

class ScatterplotLayer(Map):

    def __init__(self, 
                 data, 
                 id='ScatterplotLayer', 
                 radius=10,
                 radiusScale=1,
                 lineWidthUnits='meters',
                 lineWdithScale=1,
                 stroked=False,
                 filled=True,
                 radiusMinPixels=0,
                 radiusMaxPixels=0,
                 lineWidthMinPixels=0,
                 lineWidthMaxPixels=MAX_SAFE_INTEGER,
                 getFillColor=[255, 140, 0],
                 getLineColor=[0, 0, 0],
                 *args, 
                 **kwargs):
        super(ScatterplotLayer, self).__init__(data, id, *args, **kwargs)
        self.template = 'ScatterplotLayer'

        self.radius = radius
        self.radiusScale = radiusScale
        self.lineWidthUnits = lineWidthUnits
        self.lineWdithScale = lineWdithScale
        self.stroked = stroked
        self.filled = filled
        self.radiusMinPixels = radiusMinPixels
        self.radiusMaxPixels = radiusMaxPixels
        self.lineWidthMinPixels = lineWidthMinPixels
        self.lineWidthMaxPixels = lineWidthMaxPixels
        self.getFillColor = getFillColor
        self.getLineColor = getLineColor

    def get_options(self):
        return dict(
            data=self.data,
            id=self.id,
            radius=self.radius,
            radiusScale=self.radiusScale,
            lineWidthUnits=self.lineWidthUnits,
            lineWdithScale=self.lineWdithScale,
            stroked=self.stroked,
            filled=self.filled,
            radiusMinPixels=self.radiusMinPixels,
            radiusMaxPixels=self.radiusMaxPixels,
            lineWidthMinPixels=self.lineWidthMinPixels,
            lineWidthMaxPixels=self.lineWidthMaxPixels,
            getFillColor=self.getFillColor,
            getLineColor=self.getLineColor
        )  

"""
class GPUGridLayer(Base):

    def __init__(self,
                 data,
                 extruded=True,
                 cellSize=1000,
                 tooltip=None,
                 colorRange=['#ffffb2','#fed976','#feb24c','#fd8d3c','#f03b20','#bd0026'],
                 coverage=1,
                 #elevationDomain=,
                 elevationRange=[0, 1000],
                 elevationScale=1,
                 fp64=False,
                 gpuAggregation=True,
                 #getColorWeight=,
                 #colorAggregation=,
                 #getElevationWeight=,
                 #elevationAggregation=,
                 *args,
                 **kwargs):
        super(GPUGridLayer, self).__init__(data, *args, **kwargs)
        self.template = 'GPUGridLayer'
        self.extruded = extruded
        self.cellSize = cellSize
        self.tooltip = tooltip
        self.colorRange = colorRange
        self.coverage = coverage
        #self.elevationDomain = elevationDomain
        self.elevationRange = elevationRange,
        self.elevationScale = elevationScale
        self.fp64 = fp64
        self.gpuAggregation = gpuAggregation
        #self.getColorWeight = getColorWeight
        #self.colorAggregation = colorAggregation
        #self.getElevationWeight = getElevationWeight
        #self.elevationAggregation = elevationAggregation

    def create_html(self, filename=None):
        options = super().get_options()
        options.update(
            extruded = self.extruded,
            cellSize = self.cellSize,
            tooltip=self.tooltip,
            elevationScale=self.elevationScale,
            colorRange=self.colorRange,
            coverage=self.coverage,
            elevationRange=self.elevationRange,
            elevationScale=self.elevationScale,
            fp64=self.fp64,
            gpuAggregation=self.gpuAggregation
        )
        options = self.make_str(options)
        return templates.format(self.template, **options)
"""