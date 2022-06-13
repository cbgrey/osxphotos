""" Find photos that had an EXIF or XMP rating of 5 and mark them as favorites in Photos

    To use this script, save it to a file, e.g. `rating_to_favorites.py` then
    run it with osxphotos (https://github.com/RhetTbull/osxphotos) via
    `osxphotos run rating_to_favorites.py`

    You'll also need exiftool (https://exiftool.org/)
"""

import osxphotos
import photoscript

# only find photos taken with SONY cameras, adjust to suit your use case
CAMERA_MAKE = "SONY"


def main():
    """Find all photos with EXIF or XMP rating of 5 and mark them as favorites"""
    photosdb = osxphotos.PhotosDB()
    for photo in photosdb.photos():
        if photo.exif_info.camera_make != CAMERA_MAKE:
            continue

        # Photos stores some data in photo.exif but the rating data must be extracted with exiftool
        exif = photo.exiftool.asdict()
        # I think SONY uses XMP:Rating but also check EXIF:Rating
        xmp_rating = exif.get("XMP:Rating", 0)
        exif_rating = exif.get("EXIF:Rating", 0)
        rating = max(xmp_rating, exif_rating)
        if rating == 5:
            print(f"Marking {photo.original_filename} ({photo.uuid}) as favorite")
            photoscript.Photo(photo.uuid).favorite = True


if __name__ == "__main__":
    main()
