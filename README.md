GeoJSON diff examples
=====================

![GeoJSON diff](http://i.imgur.com/apBEgB3.png)

These are a couple of datasets I created playing with GitHub's nice
[diff visualizations for GeoJSON files][1].

There are two GeoJSON files on the `output` folder, one for members
of the United Nations and one for members of the European Union. Both are
versioned and each of the commits shows the countries that joined on a
particular year. This means that the [commit history][2] for the output
files shows the chronology of the new admissions to the UN or the EU, and that
when viewing [one particular commit][3] you can see the countries that joined
that particular year highlighted.

Countries joining on a particular year are displayed with the same fill
color, using GitHub's support of the [simplestyle][4] spec (colors are
randomly generated, so they may not look great).

The Python script `create.py` was used to generate the versioned GeoJSON
files, using data from Wikipedia (see `data` folder for more details).


[1]: https://github.com/blog/1772-diffable-more-customizable-maps
[2]: https://github.com/amercader/geojson-diff-examples/commits/master/output/un_members.geojson
[3]: http://github.com/amercader/geojson-diff-examples/commit/b1c4ec377b77a778cb1bef20f2ec53e0136d32be#diff-17ff893455bd74e9ddf39cec81d538fb
[4]: https://github.com/mapbox/simplestyle-spec
