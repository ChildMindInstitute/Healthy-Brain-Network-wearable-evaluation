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

Data and visualizations at [Open Science Framework](https://osf.io/dg869/).

# TODO:
* [ ] Compare sensors
  * [ ] accelerometer
    * [ ] ActiGraph vs E4
    * [ ] ActiGraph vs Embrace
    * [x] [ActiGraph vs GENEActiv](https://github.com/ChildMindInstitute/HBN-wearable-analysis/blob/master/short_test.ipynb)
    * [ ] ActiGraph vs Wavelet
  * [ ] photoplethysmograph
    * [ ] E4 vs Wavelet (started [here](https://github.com/ChildMindInstitute/HBN-wearable-analysis/blob/master/plot_normalized_ppgs.py) and [here](https://github.com/ChildMindInstitute/HBN-wearable-analysis/blob/master/chart_data_ppg.py))
  * [ ] EDA
    * [ ] E4 vs Embrace
  * [ ] heartrate
    * [ ] ActiGraph with Polar vs E4
    * [ ] ActiGraph with Polar vs Wavelet
    * [ ] E4 vs Wavelet
  * [ ] light
    * [ ] ActiGraph vs GENEActiv
  * [ ] temperature
    * [ ] E4 vs Embrace
    * [ ] E4 vs GENEActiv
    * [ ] Embrace vs GENEActiv
* [ ] collect comments from manufacturers
  * [x] reach out with questions
  * [ ] collect responses
* [ ] formally write up findings