while true; 

do arecord -D plughw:2,0 -d 5 -r 16000 -t wav | \
       	curl -X POST -H "Content-Type: audio/wav" --data-binary @- http://umay.develop-er.org/upload-audio?id=1 &
sleep 6

done
