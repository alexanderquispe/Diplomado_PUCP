# type: ignore
# flake8: noqa
!wget -cq --show-progress "https://github.com/alexanderquispe/Diplomado_PUCP/raw/lecture14/Lecture_14/temp/LC08_20200518_webMC.tif"

fix, ax = plt.subplots(dpi=200)

with gw.open(
    "/content/LC08_20200518_webMC.tif",

) as src:
    src.where(src !=0).plot.imshow(robust=True, ax=ax)
plt.tight_layout(pad=1)


