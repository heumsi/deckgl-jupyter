import os
import sys
import json

from IPython.core.display import HTML, display

sys.path.append(os.getcwd())

import templates
from mapboxgl.viz import MapViz
from mapboxgl.utils import *

MAX_SAFE_INTEGER = 9007199254740991
DEFAULT_COLOR_MAP = [
    [255,255,178],
    [254,217,118],
    [254,178,76],
    [253,141,60],
    [240,59,32],
    [189,0,38]
]

class Map(MapViz):

    def __init__(self, data=[], *args, **kwargs):
        super(Map, self).__init__(data, *args, **kwargs)
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
        )
    
    def as_iframe(self, html_data):
        srcdoc = html_data.replace('"', "'")
        return ('<iframe id="{div_id}", srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height};"></iframe>'.format(
                    div_id=self.div_id,
                    srcdoc=srcdoc,
                    width=self.width,
                    height=self.height
                ))

    def is_js_syntax(self, option):
        js_syntax = ['=>', 'new']
        for i in js_syntax:
            if i in option:
                return True
        return False
        

    def make_str(self, options):
        for k, v in options.items():
            if isinstance(v, str):
                if self.is_js_syntax(v):
                    continue
                elif '=>' not in v:
                    options[k] = "'{}'".format(v)
            elif isinstance(v, bool):
                options[k] = json.dumps(v)
            elif v is None:
                options[k] = json.dumps(v)
        return options

    def create_html(self, buildings=False, filename=None):

        # Create layer html
        layers = []
        for layer in self.layers:
            layer_options = layer.get_options()
            layer_options = self.make_str(layer_options)
            html = templates.format(layer.template, **layer_options)
            layers.append(html)

        # Create base html
        # Get Map Option.
        options = self.get_options()
        options = self.make_str(options)
        options['layers'] = layers
        options['buildings'] = buildings

        html = templates.format(self.template, **options)
        return html

    def show(self, **kwargs):
        # Load the HTML iframe
        html = self.create_html(**kwargs)
        map_html = self.as_iframe(html)

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))


class Base:
    
    def __init__(self,
                 data=[], 
                 id='',
                 visible=True,
                 opacity=0.8,
                 pickable=False,
                 onHover=None,
                 onClick=None,
                 onDragStart=None,
                 onDrag=None,
                 onDragEnd=None,
                 highlightColor=[0, 0, 128, 128],
                 highlightedObjectIndex=-1,
                 autoHighlight=False,
                 tooltip=None):
        self.template = 'map'
        self.defaultProps = {}

        self.data = data
        self.id = id
        self.visible = visible
        self.opacity = opacity
        self.pickable = pickable
        self.onHover = onHover
        self.onClick = onClick
        self.onDragStart = onDragStart
        self.onDrag = onDrag
        self.onDragEnd = onDragEnd
        self.highlightColor = highlightColor
        self.highlightedObjectIndex = highlightedObjectIndex
        self.autoHighlight = autoHighlight
        self.tooltip=tooltip

    def get_options(self):
        return dict(
            data = self.data,
            id = self.id,
            visible = self.visible,
            opacity = self.opacity,
            pickable = self.pickable,
            onHover = self.onHover,
            onClick = self.onClick,
            onDragStart = self.onDragStart,
            onDrag = self.onDrag,
            onDragEnd = self.onDragEnd,
            highlightColor = self.highlightColor,
            highlightedObjectIndex = self.highlightedObjectIndex,
            autoHighlight = self.autoHighlight,
            tooltip = self.tooltip
        )

class ArcLayer(Base):
    
    def __init__(self, 
                 data,
                 id='deckgl-arc',
                 widthUnits='pixels',
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 getSourcePosition='object => object.sourcePosition',
                 getTargetPosition='object => object.targetPosition',
                 getSourceColor=[0, 0, 0, 255],
                 getTargetColor=[0, 0, 0, 255],
                 getWidth=1,
                 getHeight=1,
                 getTilt=0,
                 *args, 
                 **kwargs):
        super(ArcLayer, self).__init__(data, id, *args, **kwargs)

        self.template = 'ArcLayer'
        self.widthUnits = widthUnits
        self.widthScale = widthScale
        self.widthMinPixels = widthMinPixels
        self.widthMaxPixels = widthMaxPixels
        self.getSourcePosition = getSourcePosition
        self.getTargetPosition = getTargetPosition
        self.getSourceColor = getSourceColor
        self.getTargetColor = getTargetColor
        self.getWidth = getWidth
        self.getHeight = getHeight
        self.getTilt = getTilt

    def get_options(self):
        return dict(super().get_options(), **dict(
            widthUnits=self.widthUnits,
            widthScale=self.widthScale,
            widthMinPixels=self.widthMinPixels,
            widthMaxPixels=self.widthMaxPixels,
            getSourcePosition=self.getSourcePosition,
            getTargetPosition=self.getTargetPosition,
            getSourceColor=self.getSourceColor,
            getTargetColor=self.getTargetColor,
            getWidth=self.getWidth, 
            getHeight=self.getHeight,
            getTilt=self.getTilt,
        ))

class PathLayer(Base):
    
    def __init__(self, 
                 data,
                 id='PathLayer',
                 widthUnits=1,
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 rounded=False,
                 billboard=False,
                 miterLimit=4,
                 dashJustified=False,
                 getPath='object => object.path',
                 getColor=[0, 0, 0, 255],
                 getWidth=1,
                 getDashArray=None,
                 *args, 
                 **kwargs):
        super(PathLayer, self).__init__(data, id, *args, **kwargs)

        self.template = 'PathLayer'
        self.widthUnits = widthUnits
        self.widthScale = widthScale
        self.widthMinPixels = widthMinPixels
        self.widthMaxPixels = widthMaxPixels
        self.rounded = rounded
        self.billboard = billboard
        self.miterLimit = miterLimit
        self.dashJustified = dashJustified
        self.getPath=getPath
        self.getColor=getColor
        self.getWidth=getWidth
        self.getDashArray=getDashArray

    def get_options(self):
        return dict(super().get_options(), **dict(
            widthUnits=self.widthUnits,
            widthScale=self.widthScale,
            widthMinPixels=self.widthMinPixels,
            widthMaxPixels=self.widthMaxPixels,
            rounded=self.rounded,
            billboard=self.billboard,
            miterLimit=self.miterLimit,
            dashJustified=self.dashJustified,
            getPath=self.getPath,
            getColor=self.getColor,
            getWidth=self.getWidth,
            getDashArray=self.getDashArray
        ))

class TripsLayer(PathLayer):
    
    def __init__(self, 
                 data,
                 id='TripsLayer',
                 widthUnits=1,
                 widthScale=1,
                 widthMinPixels=0,
                 widthMaxPixels=MAX_SAFE_INTEGER,
                 rounded=False,
                 billboard=False,
                 miterLimit=4,
                 dashJustified=False,
                 getPath='object => object.path',
                 getColor=[0, 0, 0, 255],
                 getWidth=1,
                 getDashArray=None,
                 currentTime=0,
                 trailLength=120,
                 *args, 
                 **kwargs):
        super(TripsLayer, self).__init__(data,
                                        id,
                                        widthUnits,
                                        widthScale,
                                        widthMinPixels,
                                        widthMaxPixels,
                                        rounded,
                                        billboard,
                                        miterLimit,
                                        dashJustified,
                                        getPath,
                                        getColor,
                                        getWidth,
                                        getDashArray,
                                        *args, **kwargs)

        self.template = 'TripsLayer'
        self.currentTime = currentTime
        self.trailLength = trailLength

    def get_options(self):
        return dict(super().get_options(), **dict(
            currentTime = self.currentTime,
            trailLength = self.trailLength
        ))


class ScatterplotLayer(Base):

    def __init__(self, 
                 data, 
                 id='ScatterplotLayer',
                 radiusScale=1,
                 lineWidthUnits='meters',
                 lineWdithScale=1,
                 stroked=False,
                 filled=True,
                 radiusMinPixels=0,
                 radiusMaxPixels=0,
                 lineWidthMinPixels=0,
                 lineWidthMaxPixels=MAX_SAFE_INTEGER,
                 getPosition='object => object.position',
                 getRadius=1,
                 getColor=[0, 0, 0, 255],
                 getFillColor=[255, 140, 0],
                 getLineColor=[0, 0, 0],
                 getLineWidth=1,
                 *args, 
                 **kwargs):
        super(ScatterplotLayer, self).__init__(data, id, *args, **kwargs)
        
        self.template = 'ScatterplotLayer'
        self.radiusScale = radiusScale
        self.lineWidthUnits = lineWidthUnits
        self.lineWdithScale = lineWdithScale
        self.stroked = stroked
        self.filled = filled
        self.radiusMinPixels = radiusMinPixels
        self.radiusMaxPixels = radiusMaxPixels
        self.lineWidthMinPixels = lineWidthMinPixels
        self.lineWidthMaxPixels = lineWidthMaxPixels
        self.getPosition = getPosition
        self.getRadius = getRadius
        self.getColor = getColor
        self.getFillColor = getFillColor
        self.getLineColor = getLineColor
        self.getLineWidth = getLineWidth

    def get_options(self):
        return dict(super().get_options(), **dict(
            radiusScale=self.radiusScale,
            lineWidthUnits=self.lineWidthUnits,
            lineWdithScale=self.lineWdithScale,
            stroked=self.stroked,
            filled=self.filled,
            radiusMinPixels=self.radiusMinPixels,
            radiusMaxPixels=self.radiusMaxPixels,
            lineWidthMinPixels=self.lineWidthMinPixels,
            lineWidthMaxPixels=self.lineWidthMaxPixels,
            getPosition=self.getPosition,
            getRadius=self.getRadius,
            getColor=self.getColor,
            getFillColor=self.getFillColor,
            getLineColor=self.getLineColor,
            getLineWidth=self.getLineWidth
        ))

class GridCellLayer(Base):

    def __init__(self, 
                 data, 
                 id='GridCellLayer', 
                 cellSize=1000,
                 coverage=1,
                 elevationScale=1,
                 extruded=True,
                 getPosition='x => x.position',
                 getColor=[255, 0, 255, 255],
                 getElevation=1000,
                 *args, 
                 **kwargs):
        super(GridCellLayer, self).__init__(data, id, *args, **kwargs)
        
        self.template = 'GridCellLayer'
        self.cellSize=cellSize
        self.coverage=coverage
        self.elevationScale=elevationScale
        self.extruded=extruded
        self.getPosition=getPosition
        self.getColor=getColor
        self.getElevation=getElevation

    def get_options(self):
        return dict(super().get_options(), **dict(
            cellSize=self.cellSize,
            coverage=self.coverage,
            elevationScale=self.elevationScale,
            extruded=self.extruded,
            getPosition=self.getPosition,
            getColor=self.getColor,
            getElevation=self.getElevation
        ))


class HeatmapLayer(Base):

    def __init__(self, 
                 data, 
                 id='HeatmapLayer', 
                 radiusPixels=30,
                 colorRange=DEFAULT_COLOR_MAP,
                 intensity=1,
                 threshold=0.05,
                 getPosition='object => object.position',
                 getWeight=1,
                 *args, 
                 **kwargs):
        super(HeatmapLayer, self).__init__(data, id, *args, **kwargs)
        
        self.template = 'HeatmapLayer'
        self.radiusPixels=radiusPixels
        self.colorRange=colorRange
        self.intensity=intensity
        self.threshold=threshold
        self.getPosition=getPosition
        self.getWeight=getWeight

    def get_options(self):
        return dict(super().get_options(), **dict(
            radiusPixels=self.radiusPixels,
            colorRange=self.colorRange,
            intensity=self.intensity,
            threshold=self.threshold,
            getPosition=self.getPosition,
            getWeight=self.getWeight,
        ))

# need to be updated.
class GridLayer(Base):

    def __init__(self, 
                 data, 
                 id='GridLayer', 
                 cellSize=1000,
                 colorDomain='[min(count), max(count)]',
                 colorRange=DEFAULT_COLOR_MAP,
                 coverage=1,
                 elevationDomain='[0, max(count)]',
                 elevationRange=[0, 1000],
                 elevationScale=1,
                 extruded=True,
                 upperPercentile=100,
                 lowerPercentile=0,
                 elevationUpperPercentile=100,
                 elevationLowerPercentile=100,
                 material='new PhongMaterial()',
                 getPosition='object => object.position',
                 getColorValue='points => points.length',
                 getColorWeight='point => 1',
                 colorAggregation='SUM',
                 getElevationValue='points => points.length',
                 getElevationWeight='point => 1',
                 elevationAggregation='SUM',
                 onSetColorDomain='() => {}',
                 onSetElevationDomain='() => {}',
                 *args, 
                 **kwargs):
        super(GridLayer, self).__init__(data, id, *args, **kwargs)
        self.template = 'GridLayer'

        self.cellSize=cellSize
        self.colorDomain=colorDomain
        self.colorRange=colorRange
        self.coverage=coverage
        self.elevationDomain=elevationDomain
        self.elevationRange=elevationRange
        self.elevationScale=elevationScale
        self.extruded=extruded
        self.upperPercentile=100
        self.lowerPercentile=0
        self.elevationUpperPercentile=100
        self.elevationLowerPercentile=100
        self.material=material
        self.getPosition=getPosition
        self.getColorValue=getColorValue
        self.getColorWeight=getColorWeight
        self.colorAggregation=colorAggregation
        self.getElevationValue=getElevationValue
        self.getElevationWeight=getElevationWeight
        self.elevationAggregation=elevationAggregation
        self.onSetColorDomain=onSetColorDomain
        self.onSetElevationDomain=onSetElevationDomain

    def get_options(self):
        return dict(super().get_options(), **dict(
            cellSize=self.cellSize,
            colorDomain=self.colorDomain,
            colorRange=self.colorRange,
            coverage=self.coverage,
            elevationDomain=self.elevationDomain,
            elevationRange=self.elevationRange,
            elevationScale=self.elevationScale,
            extruded=self.extruded,
            upperPercentile=self.upperPercentile,
            lowerPercentile=self.lowerPercentile,
            elevationUpperPercentile=self.elevationUpperPercentile,
            elevationLowerPercentile=self.elevationLowerPercentile,
            material=self.material,
            getPosition=self.getPosition,
            getColorValue=self.getColorValue,
            getColorWeight=self.getColorWeight,
            colorAggregation=self.colorAggregation,
            getElevationValue=self.getElevationValue,
            getElevationWeight=self.getElevationWeight,
            elevationAggregation= self.elevationAggregation,
            onSetColorDomain=self.onSetColorDomain,
            onSetElevationDomain=self.onSetElevationDomain
        ))

class PolygonLayer(Base):

    def __init__(self, 
                 data, 
                 id='PolygonLayer', 
                 filled=True,
                 stroked=False,
                 extruded=False,
                 wireframe=False,
                 elevationScale=1,
                 lineWidthUnits='meters',
                 lineWidthScale=1,
                 lineWidthMinPixels=0,
                 lineWidthMaxPixels=MAX_SAFE_INTEGER,
                 lineJointRounded=False,
                 lineMiterLimit=4,
                 lineDashJustified=False,
                 getPolygon='object => object.polygon',
                 getFillColor=[0, 0, 0, 255],
                 getLineColor=[0, 0, 0, 255],
                 getLineWidth=1,
                 getElevation=1000,
                 getLineDashArray=None,
                 *args, 
                 **kwargs):
        super(PolygonLayer, self).__init__(data, id, *args, **kwargs)
        
        self.template = 'PolygonLayer'
        self.filled=filled
        self.stroked=stroked
        self.extruded=extruded
        self.wireframe=wireframe
        self.elevationScale=elevationScale
        self.lineWidthUnits=lineWidthUnits
        self.lineWidthScale=lineWidthScale
        self.lineWidthMinPixels=lineWidthMinPixels
        self.lineWidthMaxPixels=lineWidthMaxPixels
        self.lineJointRounded=lineJointRounded
        self.lineMiterLimit=lineMiterLimit
        self.lineDashJustified=lineDashJustified
        self.getPolygon=getPolygon
        self.getFillColor=getFillColor
        self.getLineColor=getLineColor
        self.getLineWidth=getLineWidth
        self.getElevation=getElevation
        self.getLineDashArray=getLineDashArray

    def get_options(self):
        return dict(super().get_options(), **dict(
            filled=self.filled,
            stroked=self.stroked,
            extruded=self.extruded,
            wireframe=self.wireframe,
            elevationScale=self.elevationScale,
            lineWidthUnits=self.lineWidthUnits,
            lineWidthScale=self.lineWidthScale,
            lineWidthMinPixels=self.lineWidthMinPixels,
            lineWidthMaxPixels=self.lineWidthMaxPixels,
            lineJointRounded=self.lineJointRounded,
            lineMiterLimit=self.lineMiterLimit,
            lineDashJustified=self.lineDashJustified,
            getPolygon=self.getPolygon,
            getFillColor=self.getFillColor,
            getLineColor=self.getLineColor,
            getLineWidth=self.getLineWidth,
            getElevation=self.getElevation,
            getLineDashArray=self.getLineDashArray
        ))
