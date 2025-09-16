#!/bin/bash
# WeatherStar 4000 Music Compression Script
# This script compresses all music files to 128kbps

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed!"
    echo "Please install: sudo apt-get install ffmpeg"
    exit 1
fi

# Create temp directory
mkdir -p weatherstar_assets/music_temp

echo 'Compressing music files to 128kbps...'
echo '====================================='

echo 'Processing 1/75: smooth_jazz_01.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_01.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_01.mp3' 2>/dev/null

echo 'Processing 2/75: smooth_jazz_02.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_02.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_02.mp3' 2>/dev/null

echo 'Processing 3/75: smooth_jazz_03.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_03.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_03.mp3' 2>/dev/null

echo 'Processing 4/75: smooth_jazz_04.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_04.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_04.mp3' 2>/dev/null

echo 'Processing 5/75: smooth_jazz_05.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_05.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_05.mp3' 2>/dev/null

echo 'Processing 6/75: smooth_jazz_06.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_06.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_06.mp3' 2>/dev/null

echo 'Processing 7/75: smooth_jazz_07.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_07.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_07.mp3' 2>/dev/null

echo 'Processing 8/75: smooth_jazz_08.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_08.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_08.mp3' 2>/dev/null

echo 'Processing 9/75: smooth_jazz_09.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_09.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_09.mp3' 2>/dev/null

echo 'Processing 10/75: smooth_jazz_10.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_10.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_10.mp3' 2>/dev/null
echo '  [10/75] files processed...'

echo 'Processing 11/75: smooth_jazz_11.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_11.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_11.mp3' 2>/dev/null

echo 'Processing 12/75: smooth_jazz_12.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_12.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_12.mp3' 2>/dev/null

echo 'Processing 13/75: smooth_jazz_13.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_13.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_13.mp3' 2>/dev/null

echo 'Processing 14/75: smooth_jazz_14.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_14.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_14.mp3' 2>/dev/null

echo 'Processing 15/75: smooth_jazz_15.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_15.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_15.mp3' 2>/dev/null

echo 'Processing 16/75: smooth_jazz_16.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_16.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_16.mp3' 2>/dev/null

echo 'Processing 17/75: smooth_jazz_17.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_17.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_17.mp3' 2>/dev/null

echo 'Processing 18/75: smooth_jazz_18.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_18.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_18.mp3' 2>/dev/null

echo 'Processing 19/75: smooth_jazz_19.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_19.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_19.mp3' 2>/dev/null

echo 'Processing 20/75: smooth_jazz_20.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_20.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_20.mp3' 2>/dev/null
echo '  [20/75] files processed...'

echo 'Processing 21/75: smooth_jazz_21.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_21.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_21.mp3' 2>/dev/null

echo 'Processing 22/75: smooth_jazz_22.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_22.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_22.mp3' 2>/dev/null

echo 'Processing 23/75: smooth_jazz_23.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_23.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_23.mp3' 2>/dev/null

echo 'Processing 24/75: smooth_jazz_24.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_24.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_24.mp3' 2>/dev/null

echo 'Processing 25/75: smooth_jazz_25.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_25.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_25.mp3' 2>/dev/null

echo 'Processing 26/75: smooth_jazz_26.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_26.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_26.mp3' 2>/dev/null

echo 'Processing 27/75: smooth_jazz_27.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_27.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_27.mp3' 2>/dev/null

echo 'Processing 28/75: smooth_jazz_28.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_28.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_28.mp3' 2>/dev/null

echo 'Processing 29/75: smooth_jazz_29.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_29.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_29.mp3' 2>/dev/null

echo 'Processing 30/75: smooth_jazz_30.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_30.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_30.mp3' 2>/dev/null
echo '  [30/75] files processed...'

echo 'Processing 31/75: smooth_jazz_31.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_31.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_31.mp3' 2>/dev/null

echo 'Processing 32/75: smooth_jazz_32.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_32.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_32.mp3' 2>/dev/null

echo 'Processing 33/75: smooth_jazz_33.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_33.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_33.mp3' 2>/dev/null

echo 'Processing 34/75: smooth_jazz_34.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_34.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_34.mp3' 2>/dev/null

echo 'Processing 35/75: smooth_jazz_35.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_35.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_35.mp3' 2>/dev/null

echo 'Processing 36/75: smooth_jazz_36.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_36.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_36.mp3' 2>/dev/null

echo 'Processing 37/75: smooth_jazz_37.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_37.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_37.mp3' 2>/dev/null

echo 'Processing 38/75: smooth_jazz_38.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_38.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_38.mp3' 2>/dev/null

echo 'Processing 39/75: smooth_jazz_39.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_39.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_39.mp3' 2>/dev/null

echo 'Processing 40/75: smooth_jazz_40.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_40.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_40.mp3' 2>/dev/null
echo '  [40/75] files processed...'

echo 'Processing 41/75: smooth_jazz_41.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_41.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_41.mp3' 2>/dev/null

echo 'Processing 42/75: smooth_jazz_42.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_42.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_42.mp3' 2>/dev/null

echo 'Processing 43/75: smooth_jazz_43.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_43.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_43.mp3' 2>/dev/null

echo 'Processing 44/75: smooth_jazz_44.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_44.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_44.mp3' 2>/dev/null

echo 'Processing 45/75: smooth_jazz_45.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_45.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_45.mp3' 2>/dev/null

echo 'Processing 46/75: smooth_jazz_46.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_46.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_46.mp3' 2>/dev/null

echo 'Processing 47/75: smooth_jazz_47.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_47.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_47.mp3' 2>/dev/null

echo 'Processing 48/75: smooth_jazz_48.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_48.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_48.mp3' 2>/dev/null

echo 'Processing 49/75: smooth_jazz_49.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_49.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_49.mp3' 2>/dev/null

echo 'Processing 50/75: smooth_jazz_50.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_50.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_50.mp3' 2>/dev/null
echo '  [50/75] files processed...'

echo 'Processing 51/75: smooth_jazz_51.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_51.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_51.mp3' 2>/dev/null

echo 'Processing 52/75: smooth_jazz_52.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_52.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_52.mp3' 2>/dev/null

echo 'Processing 53/75: smooth_jazz_53.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_53.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_53.mp3' 2>/dev/null

echo 'Processing 54/75: smooth_jazz_54.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_54.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_54.mp3' 2>/dev/null

echo 'Processing 55/75: smooth_jazz_55.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_55.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_55.mp3' 2>/dev/null

echo 'Processing 56/75: smooth_jazz_56.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_56.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_56.mp3' 2>/dev/null

echo 'Processing 57/75: smooth_jazz_57.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_57.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_57.mp3' 2>/dev/null

echo 'Processing 58/75: smooth_jazz_58.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_58.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_58.mp3' 2>/dev/null

echo 'Processing 59/75: smooth_jazz_59.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_59.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_59.mp3' 2>/dev/null

echo 'Processing 60/75: smooth_jazz_60.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_60.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_60.mp3' 2>/dev/null
echo '  [60/75] files processed...'

echo 'Processing 61/75: smooth_jazz_61.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_61.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_61.mp3' 2>/dev/null

echo 'Processing 62/75: smooth_jazz_62.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_62.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_62.mp3' 2>/dev/null

echo 'Processing 63/75: smooth_jazz_63.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_63.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_63.mp3' 2>/dev/null

echo 'Processing 64/75: smooth_jazz_64.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_64.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_64.mp3' 2>/dev/null

echo 'Processing 65/75: smooth_jazz_65.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_65.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_65.mp3' 2>/dev/null

echo 'Processing 66/75: smooth_jazz_66.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_66.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_66.mp3' 2>/dev/null

echo 'Processing 67/75: smooth_jazz_67.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_67.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_67.mp3' 2>/dev/null

echo 'Processing 68/75: smooth_jazz_68.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_68.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_68.mp3' 2>/dev/null

echo 'Processing 69/75: smooth_jazz_69.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_69.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_69.mp3' 2>/dev/null

echo 'Processing 70/75: smooth_jazz_70.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_70.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_70.mp3' 2>/dev/null
echo '  [70/75] files processed...'

echo 'Processing 71/75: smooth_jazz_71.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_71.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_71.mp3' 2>/dev/null

echo 'Processing 72/75: smooth_jazz_72.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_72.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_72.mp3' 2>/dev/null

echo 'Processing 73/75: smooth_jazz_73.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_73.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_73.mp3' 2>/dev/null

echo 'Processing 74/75: smooth_jazz_74.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_74.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_74.mp3' 2>/dev/null

echo 'Processing 75/75: smooth_jazz_75.mp3'
ffmpeg -i 'weatherstar_assets/music/smooth_jazz_75.mp3' -b:a 128k -ar 44100 -ac 2 -y 'weatherstar_assets/music_temp/smooth_jazz_75.mp3' 2>/dev/null


# Replace original files with compressed ones
echo 'Replacing original files...'
rm -f weatherstar_assets/music/*.mp3
mv weatherstar_assets/music_temp/*.mp3 weatherstar_assets/music/
rmdir weatherstar_assets/music_temp

echo '====================================='
echo '✓ Compression complete!'
echo 'All files compressed to 128kbps'

# Show new size
echo ''
echo 'New total size:'
du -sh weatherstar_assets/music/
