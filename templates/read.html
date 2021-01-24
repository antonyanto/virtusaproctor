<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Audio/Video Example - Record Plugin for Video.js</title>

        <!-- Include Video.js stylesheet (https://videojs.com/) -->
        <link href="../node_modules/video.js/dist/video-js.min.css" rel="stylesheet">

        <!-- Style of VideoJS -->
        <link href="../dist/css/videojs.record.css" rel="stylesheet">

        <style>
        /* change player background color */
        #myVideo {
            background-color: #9ab87a;
        }
        </style>
    </head>
    <body>
        <!-- Create the preview video element -->
        <video id="myVideo" class="video-js vjs-default-skin"></video>

        <!-- Load video.js -->
        <script src="../node_modules/video.js/dist/video.min.js"></script>

        <!-- Load RecordRTC core and adapter -->
        <script src="../node_modules/recordrtc/RecordRTC.js"></script>
        <script src="../node_modules/webrtc-adapter/out/adapter.js"></script>

        <!-- Load VideoJS Record Extension -->
        <script src="../dist/videojs.record.js"></script>
        <script>
        var videoMaxLengthInSeconds = 120;

        // Inialize the video player
        var player = videojs("myVideo", {
            controls: true,
            width: 720,
            height: 480,
            fluid: false,
            plugins: {
                record: {
                    audio: true,
                    video: true,
                    maxLength: videoMaxLengthInSeconds,
                    debug: true,
                    videoMimeType: "video/webm;codecs=H264"
                }
            }
        }, function(){
            // print version information at startup
            videojs.log(
                'Using video.js', videojs.VERSION,
                'with videojs-record', videojs.getPluginVersion('record'),
                'and recordrtc', RecordRTC.version
            );
        });

        // error handling for getUserMedia
        player.on('deviceError', function() {
            console.log('device error:', player.deviceErrorCode);
        });

        // Handle error events of the video player
        player.on('error', function(error) {
            console.log('error:', error);
        });

        // user clicked the record button and started recording !
        player.on('startRecord', function() {
            console.log('started recording! Do whatever you need to');
        });

        // user completed recording and stream is available
        // Upload the Blob to your server or download it locally !
        player.on('finishRecord', function() {

            // the blob object contains the recorded data that
            // can be downloaded by the user, stored on server etc.
            var videoBlob = player.recordedData.video;

            console.log('finished recording: ', videoBlob);
        });
        </script>
    </body>
</html>
