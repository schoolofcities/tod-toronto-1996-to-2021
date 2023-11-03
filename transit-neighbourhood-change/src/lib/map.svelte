<script>
    import { onMount, afterUpdate } from "svelte";
    import maplibregl from "maplibre-gl";
    import transit_line from "../data/transit-lines.geo.json";
    import transit_point from "../data/transit-point.geo.json";
    import transit_station from "../data/transit-station.geo.json";
    import transit_line_bold from "../data/transit-lines.geo.json";
    //import notVancouverPolygon from '../../data/not-vancouver-polygon.geo.json';
    console.log(transit_point);
    let map;
    let popupContent = false;

    function hidePopup() {
        popupContent = false;
    }
    export let transitName
    let coordinates;
    let title;
    let description;
    let type;
    let status;
    let siteaddress;
    let primarymaterial;
    const photoURL =
        "https://opendata.vancouver.ca/explore/dataset/public-art/files/";
    let photoID;
    let year;

    onMount(() => {
        /*const maxBounds = [ 
        [-123.8, 49.0], //SW coords
        [-122.6, 49.5] //NE coords
      ];*/

        map = new maplibregl.Map({
            container: "map",
            style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json", //'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
            center: [-79.4, 43.68], // starting position
            zoom: 11, // starting zoom;
            minZoom: 2,
            maxZoom: 17,
            projection: "globe",
            scrollZoom: true,
            attributionControl: false,
        });

        // Adding scale bar to the map
        let scale = new maplibregl.ScaleControl({
            maxWidth: 100,
            unit: "metric",
        });
        map.addControl(scale, "bottom-left");

        // Adding zoom and rotation controls to the map
        map.addControl(new maplibregl.NavigationControl(), "top-right");

        // Adding additional layers from geojson
        map.on("load", function () {
            const layers = map.getStyle().layers;

            // Find the index of the first symbol layer in the map style.
            let firstSymbolId;
            for (const layer of layers) {
                if (layer.type === "symbol") {
                    firstSymbolId = layer.id;
                    break;
                }
            }

            map.addSource("transit_line", {
                type: "geojson",
                data: transit_line,
            });
  
            map.addSource("transit_point", {
                type: "geojson",
                data: transit_point,
            });

            map.addSource("transit_line_bold", {
                type: "geojson",
                data: transit_line_bold,
            });

            map.addLayer(
                {
                    id: "transit_line_bold",
                    type: "line",
                    source: "transit_line_bold",
                    layout: {},
                    'filter': ['==', 'NAME', transitName],
                    paint: {
                        "line-color": [
                            "match",
                            ["get", "NAME"],
                            "Yonge-University Subway",
                            "#F1C500",
                            "Spadina Subway Extension",
                            "#F1C500",
                            "Yonge North Subway Extension",
                            "#F1C500",
                            "Bloor-Danforth Subway",
                            "#16A753",
                            "Scarborough Subway",
                            "#16A753",
                            "Scarborough RT",
                            "#1F99D5",
                            "Sheppard Subway",
                            "#B32078",
                            "Sheppard East",
                            "#B32078",
                            "Eglinton Crosstown LRT",
                            "#F87005",
                            "Finch West LRT",
                            "#888888",
                            "Ontario Line",
                            "#000000",
                            "#FFFFFF",
                        ],
                        "line-width": 5,
                    },
                }
                //before: "transit_line",
            );
            
            map.addLayer(
                {
                    id: "transit_line",
                    type: "line",
                    source: "transit_line",
                    layout: {},
                    paint: {
                        "line-color": [
                            "match",
                            ["get", "NAME"],
                            "Yonge-University Subway",
                            "#F1C500",
                            "Spadina Subway Extension",
                            "#F1C500",
                            "Yonge North Subway Extension",
                            "#F1C500",
                            "Bloor-Danforth Subway",
                            "#16A753",
                            "Scarborough Subway",
                            "#16A753",
                            "Scarborough RT",
                            "#1F99D5",
                            "Sheppard Subway",
                            "#B32078",
                            "Sheppard East",
                            "#B32078",
                            "Eglinton Crosstown LRT",
                            "#F87005",
                            "Finch West LRT",
                            "#888888",
                            "Ontario Line",
                            "#000000",
                            "#FFFFFF",
                        ],
                        "line-width": 2,
                    },
                }
                //before: "transit_line",
            );
           
            map.addLayer({
                id: "transit_point",
                type: "circle",
                source: "transit_point",
                layout: {},
                paint: {
                    "circle-color": [
                        "match",
                        ["get", "NAME"],
                        "Yonge-University Subway",
                        "#F1C500",
                        "Spadina Subway Extension",
                        "#F1C500",
                        "Yonge North Subway Extension",
                        "#F1C500",
                        "Bloor-Danforth Subway",
                        "#16A753",
                        "Scarborough Subway",
                        "#16A753",
                        "Scarborough RT",
                        "#1F99D5",
                        "Sheppard Subway",
                        "#B32078",
                        "Sheppard East",
                        "#B32078",
                        "Eglinton Crosstown LRT",
                        "#F87005",
                        "Finch West LRT",
                        "#888888",
                        "Ontario Line",
                        "#000000",
                        "#FFFFFF",
                    ],
                    "circle-radius": 7,
                },
                before: "transit_line",
            });
        });
        /*
        // Create pop-up
        const popup = new maplibregl.Popup({
            closeButton: true,
            closeOnClick: true,
            maxWidth: "none",
        });

        map.on("mouseenter", "vancouverPublicArt", () => {
            map.getCanvas().style.cursor = "pointer";
        });

        map.on("mouseleave", "vancouverPublicArt", () => {
            map.getCanvas().style.cursor = "";
        });
        
        map.on("click", "vancouverPublicArt", (e) => {
            map.flyTo({
                center: e.features[0].geometry.coordinates,
                zoom: 17,
            });

            $: coordinates = e.features[0].geometry.coordinates.slice();
            $: title = e.features[0].properties.title_of_work;
            $: description = e.features[0].properties.descriptionofwork;
            $: type = e.features[0].properties.type;
            $: status = e.features[0].properties.status;
            $: siteaddress = e.features[0].properties.siteaddress;
            $: primarymaterial = e.features[0].properties.primarymaterial;
            // $: photoURL = "https://opendata.vancouver.ca/explore/dataset/public-art/files/";
            $: photoID = JSON.parse(e.features[0].properties.photourl).id;
            $: year = e.features[0].properties.yearofinstallation;

            // Organize popup information
            // const htmlContent =
            // "<h1 id='pt'>" + title + "</h1>" +
            // "<p> <img src='" + photoURL + photoID + "/download/' width=300 height=240> </p>" +
            // "<p> <b>Description: </b>" + description + "</p>" +
            // "<p> <b>Type: </b>" + type + "</p>" +
            // "<p> <b>Current Status: </b>" + status + "</p>" +
            // "<p> <b>Primary Material: </b>" + primarymaterial + "</p>" +
            // "<p> <b>Address: </b>" + siteaddress + "</p>" +
            // "<p> <b>Year of Installation: </b>" + year + "</p>";

            // Populate the popup
            popup.setLngLat(coordinates);
            popupContent = true;
            //document.getElementById('popup').innerHTML = htmlContent;
        }); */
    });

    $: if (popupContent) {
        console.log(photoURL + "/" + photoID + "/download/");
    }
</script>

<main>
    <div id="map" />

</main>

<style>
    main {
        overflow-y: hidden;
        max-width: 80%;
        max-height: 40vw;
    }

    @font-face {
        font-family: TradeGothicBold;
        src: url("../assets/Trade Gothic LT Bold.ttf");
    }
    @font-face {
        font-family: RobotoRegular;
        src: url("../assets/Roboto-Regular.ttf");
    }

    #map {
        padding-top: 5%;
        height: 100vh;
        width: 100%;
        top: 0;
        left: 0;
        position: relative;
    }

    .popup {
        position: absolute;
        top: 145px;
        left: 10px;
        width: 290px; /* Set a fixed width for the popup */
        max-height: calc(
            100% - 200px
        ); /* Calculate the max height based on viewport height */
        /* overflow-y: scroll;  */
        background-color: rgb(254, 251, 249, 0.9);
        padding: 0px;
        padding-top: 15px;
        padding-left: 10px;
        padding-right: 20px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
        overflow-x: hidden;
    }

    #hide {
        position: absolute;
        height: 15px;
        width: 100%;
        padding: 0px;
        margin: 0px;
        top: 0px;
        left: 0px;
        font-family: TradeGothicBold;
        font-size: 12px;
        color: #9da9bd;
        background-color: none;
        border-bottom: solid 1px rgb(227, 227, 227);
        z-index: 9999;
        text-align: center;
    }
    #hide:hover {
        color: #dc4633;
        cursor: pointer;
    }

    h2 {
        font-size: 24px;
        font-family: TradeGothicBold;
        padding: 2px;
        margin: 0px;
        margin-top: 8px;
        /* margin-bottom: -4px; */
        color: #00a189;
        background: linear-gradient(135deg, #f1c50055 25%, transparent 25%) -4px
                0/ 8px 8px,
            linear-gradient(225deg, #f1c50032 25%, transparent 25%) -4px 0/ 8px
                8px,
            linear-gradient(315deg, #f1c50055 25%, transparent 25%) 0px 0/ 8px 8px,
            linear-gradient(45deg, #f1c50044 25%, #ffffff 25%) 0px 0/ 8px 8px;
        /* -webkit-text-stroke: 1px #6FC7EA; */
    }

    #subtitle {
        font-family: TradeGothicBold;
        color: #1e3765;
        font-size: 16px;
    }

    p {
        font-family: RobotoRegular;
        font-size: 13px;
        opacity: 1;
        color: #1e3765;
    }

</style>
