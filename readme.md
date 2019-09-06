## Script Deckgl for Jupyter Notebook

Deckgl-jupyter 는 위치 데이터 시각화 라이브러리인 Deck.gl 을 쥬피터 노트북 에서도 쓸 수 있게 만든 라이브러리 입니다. 

예를 들어, 쥬피터 노트북에서 아래와 같은 방법으로 사용가능합니다.

![image-20190906164759155](/Users/heumsi/Library/Application Support/typora-user-images/image-20190906164759155.png)



현재까지 제공되는 레이어는 다음과 같습니다.

- Arc Layer
- Polygon Layer
- Path Layer
- Trips Layer
- ScatterPlot Layer
- Grid Layer
- GridCell Layer
- Heatmap Layer

Heatmap Layer 의 경우, WebGL2 가 미설치된 브라우저 상황에 따라 작동하지 않을 수 있습니다.
렌더링 부분은 전적으로 Deck.gl 버전을 따라가기에, Deck.gl 에서 해결되지 않은 이슈와 버그가 이 패키지에서도 존재할 수 있습니다.
현재 적용하고 있는 Deck.gl 버전은 **deck.gl@7.2.0** 입니다.



다음과 같은 특징이 있습니다.

- Mapbox Basemap 을 사용합니다. 따라서, Mapbox Map 에 사용되는 파라미터들을 사용할 수 있습니다.
- Mapbox-gl-language 가 기본적으로 Add-on 되어있습니다. 
  따라서, Basemap 언어가 지역에 따라 알아서 바뀝니다.
- Mapboxgl_jupyter 의 경우, 하나의 맵에 여러 개의 Layer 쌓는 것이 불가능했습니다.
  하지만 이 패키지에서는 가능합니다.
- 이 패키지는 Deck.gl의 기능들을 구현하되,
  코드는 Mapboxgl_jupyter 를 본 떠 만들었고,
  사용 스타일은 Deck.gl과 Folium 스럽게 만들었습니다.



현재 Uber 팀에서 deck.gl 의 공식 python 패키지인 [pydeck](https://github.com/uber/deck.gl/tree/master/bindings/python/pydeck) 을 준비하고 있습니다만, 보다 가볍고 빠르게 사용하기 위해, 해당 패키지를 개발했습니다. 아무래도, pydeck 이 제대로 릴리즈 되기 전까지 임시로 deck.gl의 기능들을 사용해볼 수 있는 패키지가 될 듯 합니다.



## Installation

```bash
pip install deckgl_jupyter
```

또는

```bash
git clone https://github.com/heumsi/deckgl_jupyter.git
...

python setup.py build
python setup.py install
```



## Usage

기본적으로 Deck.gl 사용법과 동일합니다.

[Example.ipynb](https://github.com/heumsi/deckgl_jupyter/blob/master/Examples.ipynb) 를 통해, 어떻게 쓰는지 금방 감을 잡으실 수 있을 것이고,
각 레이어의 파라미터는 [Deck.gl api reference](https://deck.gl/#/documentation/deckgl-api-reference/layers/layer) 에서 확인하실 수 있습니다.



## Development & Issue

이 패키지는, 사실 제가 시각화 하는 과정에 답답함을 느껴, 원하는대로 사용하고자 빠르게 만든 패키지입니다.
따라서, 아직 부족한게 매우매우 많습니다.
코드를 보시면 아시겠지만, Deck.gl 에는 존재하지만 지금 당장 필요해보이지 않는 레이어의 일부 파라미터들은 코드에 아예 없거나 주석처리 되어있습니다. 따라서, 사용 중에 뭔가 이상하다 싶으면, 코드를 확인해서, 해당 파라미터가 존재하는지 확인해주시기 바랍니다. 다만, 대부분 시각화와 분석하는데 사용되지 않을 것 같은 파라미터들이라고 생각됩니다.

이슈와 추가 개발은 언제든지 환영입니다.
코드는 어렵지 않고, 조금 노가다성을 띄고 있습니다.
Deck.gl 에는 있는데 여기에는 없는 코드, 버그가 있는 코드, 리팩토링 등 수정은 언제든지 부탁드립니다.