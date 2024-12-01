while true; 

do   arecord -D plughw:2,0 -d 5 -f cd -t wav | curl -X POST -H "Content-Type: audio/wav" --data-binary @- http://umay.develop-er.org/upload-audio;

sleep 1

done
