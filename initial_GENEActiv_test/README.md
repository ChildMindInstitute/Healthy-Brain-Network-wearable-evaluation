README
================

GENEActiv\_analysis.R: Script to analyze output binary files from GENEActive wearable devices.

Built in R 3.3.2 (Sincere Pumpkin Patch)

Author: – Jon Clucas, 2017 <jon.clucas@childmind.org>

© 2017, Child Mind Institute, Apache v2.0 License

Depends on: Package 'GENEAread' v 1.1.1 Maintainer: Joss Langford <Joss at activinsights.co.uk> Author: – Zhou Fang Published: 2013-04-23 License: GPL-2 | GPL-3 Documentation: <https://cran.r-project.org/web/packages/GENEAread/GENEAread.pdf>

Package 'GGIR' v 1.4 Author: – Vincent T van Hees <vincentvanhees@gmail.com> Contributors: – Zhou Fang – Jing Hua Zhao – Joe Heywood – Severine Sabia Date/Publication: 2017-01-22 17:02:09 License: LGPL (≥ 2.0, &lt; 3) Documentation: <https://cran.r-project.org/web/packages/GGIR/GGIR.pdf>

The relative timecost of processing does appear to decrease with increased recording frequency, although the absolute timecost naturally rises. Here are the processing times of two iterations of processing the same five binary files.

arno\_foot\_l : 85.7 Hz : 48 hrs : Processing took: 2.219 mins . Loaded 14803200 records (Approx 829 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 16:58:24.488 (Wed) Processing took: 39.367 secs . Loaded 14803200 records (Approx 829 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 16:58:24.488 (Wed)

arno\_foot\_r : 60.0 Hz : 48 hrs: Processing took: 3.077 mins . Loaded 10368000 records (Approx 581 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 17:00:00.483 (Wed) Processing took: 25.765 secs . Loaded 10368000 records (Approx 581 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 17:00:00.483 (Wed)

arno\_hand : 30.0 Hz : 168 hrs: Processing took: 3.916 secs . Loaded 2009100 records (Approx 113 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-21 12:31:58.964 (Tue) Processing took: 3.652 secs . Loaded 2009100 records (Approx 113 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-21 12:31:58.964 (Tue)

curt\_hand : 100.0 Hz : 168 hrs: Processing took: 12.753 mins . Loaded 33276000 records (Approx 1863 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-24 13:26:00.490 (Fri) Processing took: 9.103 mins . Loaded 33276000 records (Approx 1863 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-24 13:26:00.490 (Fri)

jon\_hand : 10.0 Hz : 48 hrs: Processing took: 3.57 secs . Loaded 1728000 records (Approx 97 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 17:00:00.400 (Wed) Processing took: 3.991 secs . Loaded 1728000 records (Approx 97 MB of RAM) 17-02-20 17:00:00.500 (Mon) to 17-02-22 17:00:00.400 (Wed)

``` r
plot(meta$record_frames, meta$processing_times, xlab = "number of frames captured", ylab = "processing time", main="Processing Time by number of frames captured, 2 trials")
abline(lm(meta$processing_times ~ meta$record_frames))
points(meta$record_frames, meta$pt2, pch = 2, col="#0067a0")
abline(lm(meta$pt2 ~ meta$record_frames), col="#0067a0")
```

![](README_files/figure-markdown_github/plot%20processing%20time-1.png)

``` r
ggplot(acc_data, aes(x=timestamp, y=light)) + geom_point(aes(col=factor(
       device), shape=factor(device))) + labs(title = 
       "Light exposure over time by device")
```

![](README_files/figure-markdown_github/plot%20light%20over%20time%20by%20device-1.png)
