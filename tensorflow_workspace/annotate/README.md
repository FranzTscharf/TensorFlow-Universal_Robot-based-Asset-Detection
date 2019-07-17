# Generate Annotations
## Python script
einfach das Model im Ordner "pre-trained-model" austauschen und in dem ordner annotations die label map ändern und die Bilder im order Test ersetzen um ein eigenes Model für das annotieren von bildern zu verwenden
## Run
```
python annotate.py
```
Nun werden für die Bilder im Ordner ./test die annotationen durch das pre-trained model hinzugefügt.

## Source

Diese Repository basiert auf dem Prinzip aus dem artikel:
http://andrew.carterlunn.co.uk/programming/2018/01/24/annotating-large-datasets-with-tensorflow-object-detection-api.html