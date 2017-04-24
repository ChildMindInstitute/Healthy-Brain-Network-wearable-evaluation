# HBN-wearable-analysis
Analyses for HBN wearable devices

We are comparing the following devices:

* [ActiGraph wGT3X-BT](http://actigraphcorp.com/products-showcase/activity-monitors/actigraph-wgt3x-bt/)
* [Empatica E4](https://www.empatica.com/e4-wristband)
* [Empatica Embrace](https://www.empatica.com/product-embrace)
* [GENEActiv Original](https://www.geneactiv.org/actigraphy/geneactiv-original/)
* [Wavelet Wristband](https://wavelethealth.com/products/)

We are comparing the following sensors:

sensor | unit | devices
------ | ---- | -------
accelerometer and/or gyroscope | standard acceleration due togravity (g) | ActiGraph, E4, Embrace, GENEActiv, Wavelet
photoplethysmograph | nanowatt (nW) | E4, Wavelet
electrodermal activity | microsiemens (μS) | E4, Embrace
heartrate | beats per minute (bpm) | ActiGraph (with [Polar H7](http://actigraphcorp.com/products/bluetooth-heart-rate-monitor/) electrocardiograph), E4 (with ppg), Wavelet (with ppg)
light | lux (lx) | ActiGraph, GENEActiv
temperature | degrees Celcius (°C) | Embrace, E4, GENEActiv

[![](line_charts/normalized_acc_GENEActiv_and_Actigraph_ba.png)](https://osf.io/bkv6s/)

[![](line_charts/normalized_acc_GENEActiv_and_Actigraph_zba.png)](https://osf.io/yfpn9/)

[![](line_charts/2017-04-07_Arno_right.png)](https://osf.io/4fj9t/)

Data and visualizations at [Open Science Framework](https://osf.io/dg869/).

# TODO:
* [ ] Compare sensors
  * [x] accelerometer
  * [ ] photoplethysmograph (started [here](https://github.com/ChildMindInstitute/HBN-wearable-analysis/blob/master/plot_normalized_ppgs.py) and [here](https://github.com/ChildMindInstitute/HBN-wearable-analysis/blob/master/chart_data_ppg.py)
  * [ ] EDA
  * [ ] heartrate
  * [ ] light
  * [ ] temperature
* [ ] collect comments from manufacturers
  * [x] reach out with questions
  * [ ] collect responses
* [ ] formally write up findings