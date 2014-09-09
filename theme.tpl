<!DOCTYPE html>
<html>
    <head>
        <meta content="text/html;charset=utf-8" http-equiv="Content-Type" />
        <title>Jeroboam</title>
        <meta name="author" content="Jeroboam" />
        <link href='http://fonts.googleapis.com/css?family=Lato:300|Open+Sans+Condensed:300' rel='stylesheet' type='text/css'>
        <style type="text/css">
            html { -ms-touch-action: manipulation; touch-action: manipulation; }
            body { background:#222; color:#DDD; margin:0; padding:0; border:0; width:100%; font-family: 'Lato', sans-serif; }
            #main { clear:both; margin:0px; padding:0px; }
            #main:before, #main:after { content:""; display:table; }
            #main:after { clear:both; }
            .column { display: block; float:left; margin: 0 1%; }
            #left { width: 20%; padding:1em 0; background-color:#444; }
            #left ul { list-style:none; margin:2em 1em; padding:0; }
            #left ul li { margin-bottom:1em; list-style-position:inside; white-space: nowrap;
                          overflow: hidden; text-overflow: ellipsis; }
            #left ul li a { color:#DDD; text-decoration:none; }
            header { text-align:center; font-size:30px; font-family: 'Open Sans Condensed', sans-serif; }
            footer { text-align:center; font-size:12px; }
            header a, footer a { color:#DDD; text-decoration:none; }
            #right { width: 76%; margin-top:1em; }
            .picture { text-align:center; display:-moz-box; }
            #nopictures { text-align:center; margin:3em; font-size:2em; background-color:#444; height: 3em;
                          border-radius: 10px 10px 10px 10px; -moz-border-radius: 10px 10px 10px 10px; -webkit-border-radius: 10px 10px 10px 10px; }

            /* imagelightbox */
            #main img { margin:1em; border:0.5em solid #444; }
            #main img:hover, #main img:focus { border-color: #DDD; }

            #imagelightbox { cursor:pointer; position:fixed; z-index:10000; -ms-touch-action:none; touch-action:none; }
            #imagelightbox-overlay { background-color:rgba( 80, 80, 80, .9 ); position:fixed; z-index:9998; top:0; right:0; bottom:0; left:0; }

            #imagelightbox-close { width:2.5em; height:2.5em; text-align:left; background-color:#666; border-radius:50%; position:fixed; z-index:10002; top: 2.5em; right: 2.5em; -webkit-transition: color .3s ease; transition: color .3s ease; }
            #imagelightbox-close:hover, #imagelightbox-close:focus { background-color: #111; }
            #imagelightbox-close:before, #imagelightbox-close:after { width: 2px; background-color: #fff; content: ''; position: absolute;
                                                                      top: 20%; bottom: 20%; left: 50%; margin-left: -1px; }
            #imagelightbox-close:before { -webkit-transform: rotate( 45deg ); -ms-transform: rotate( 45deg ); transform: rotate( 45deg ); }
            #imagelightbox-close:after { -webkit-transform: rotate( -45deg ); -ms-transform: rotate( -45deg ); transform: rotate( -45deg ); }

            #imagelightbox-overlay, #imagelightbox-close { -webkit-animation: fade-in .25s linear; animation: fade-in .25s linear; }
            @-webkit-keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
            @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }

            @media only screen and (max-width: 480px) {
                .col { margin: 1% 0; }
                #left, #right { width: 100%; }
                #main { width: 100%; }
                #imagelightbox-close { top: 1.25em; right: 1.25em; }
            }

        </style>
    </head>
    <body>

    <div id="main">
        <div id="left" class="column">
            <header><a href="/">JEROBOAM</a></header>
            <ul>
                % for folder in tree:
                    % if folder:
                        % space = '&nbsp;' * 3 * len([slash for slash in folder if slash == '/'])
                        % folder_text = folder.split('/')[-1]
                        <li><a href="/{{folder}}">{{!space}}{{folder_text}}</a></li>
                    % end
                % end
            </ul>
            % from time import strftime
            % date = strftime("%Y-%m-%d %H:%M:%S")
            <footer><a href="http://github.com">Generated by Jeroboam on {{date}}.</a></footer>
        </div>
        <div id="right" class="column">
            % for pic in pictures:
                % pic_text = pic.split('/')[-1]
                <div class="picture">
                    <a data-imagelightbox="X" href="/{{pic}}"><img src="/cache/{{pic}}" /></a><br />{{pic_text}}
                </div>
            % end
        </div>
    </div>

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="/imagelightbox.min.js"></script>
    <script>
        $( function() {
            overlayOn = function() { $( '<div id="imagelightbox-overlay"></div>' ).appendTo( 'body' ); },
            overlayOff = function() { $( '#imagelightbox-overlay' ).remove(); },
            closeButtonOn = function( instance ) {
                $( '<button type="button" id="imagelightbox-close" title="Close"></button>' ).appendTo('body').on('click touchend', function(){ $(this).remove(); instance.quitImageLightbox(); return false; });
            },
            closeButtonOff = function() { $( '#imagelightbox-close' ).remove(); }

            var selector = 'a[data-imagelightbox="X"]';
            var instance = $( selector ).imageLightbox({
                quitOnImgClick: false,
                onStart: function() { overlayOn(); closeButtonOn(instance); },
                onEnd:   function() { overlayOff(); closeButtonOff(); }
            });
        });
    </script>

    </body>
</html>
