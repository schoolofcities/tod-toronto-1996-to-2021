<script>
    import { onMount, afterUpdate } from "svelte";
    import maplibregl from "maplibre-gl";
    import transit_line from "../data/transit-lines.geo.json";
    import transit_station from "../data/transit-station.geo.json";
    import transit_line_bold from "../data/transit-lines.geo.json";
    //import notVancouverPolygon from '../../data/not-vancouver-polygon.geo.json';

    let map;

    export let transitName;

    const photoURL =
        "https://opendata.vancouver.ca/explore/dataset/public-art/files/";

    onMount(() => {
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

            map.addSource("transit_station", {
                type: "geojson",
                data: transit_station,
            });

            map.addSource("transit_line_bold", {
                type: "geojson",
                data: transit_line_bold,
            });

            map.addLayer(
                {
                    id: "transit-line-bold-ID",
                    type: "line",
                    source: "transit_line_bold",
                    layout: {},
                    filter: ["==", "NAME", transitName],
                    paint: {
                        "line-color": [
                            "match",
                            ["get", "NAME"],
                            "Line 1: Yonge-University Subway",
                            "#F1C500",
                            "Yonge North Subway Extension",
                            "#F1C500",
                            "Line 2: Bloor-Danforth Subway",
                            "#16A753",
                            "Scarborough Subway Extension",
                            "#16A753",
                            "Line 3: Scarborough RT",
                            "#1F99D5",
                            "Line 4: Sheppard Subway",
                            "#B32078",
                            "Eglinton Crosstown LRT",
                            "#F87005",
                            "Eglinton Crosstown West Extension",
                            "#F87005",
                            "Eglinton East LRT",
                            "#F87005",
                            "Eglinton Crosstown West Extension - Airport Segment",
                            "#F87005",
                            "Finch West LRT",
                            "#888888",
                            "Ontario Line",
                            "#000000",
                            "#FFFFFF",
                        ],
                        "line-width": 5,
                    },
                    before: "transit-station-ID",
                }
                //before: "transit_line",
            );

            map.addLayer(
                {
                    id: "transit-line-ID",
                    type: "line",
                    source: "transit_line",
                    layout: {},
                    paint: {
                        "line-color": [
                            "match",
                            ["get", "NAME"],
                            "Line 1: Yonge-University Subway",
                            "#F1C500",
                            "Yonge North Subway Extension",
                            "#F1C500",
                            "Line 2: Bloor-Danforth Subway",
                            "#16A753",
                            "Scarborough Subway Extension",
                            "#16A753",
                            "Line 3: Scarborough RT",
                            "#1F99D5",
                            "Line 4: Sheppard Subway",
                            "#B32078",
                            "Eglinton Crosstown LRT",
                            "#F87005",
                            "Eglinton Crosstown West Extension",
                            "#F87005",
                            "Eglinton East LRT",
                            "#F87005",
                            "Eglinton Crosstown West Extension - Airport Segment",
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
                id: "transit-station-ID",
                type: "circle",
                source: "transit_station",
                filter: ["==", "NAME", transitName],
                paint: {
                    "circle-color": "#FFFFFF",
                    "circle-radius": 4,
                    "circle-stroke-color": [
                        "match",
                        ["get", "NAME"],
                        "Line 1: Yonge-University Subway",
                        "#F1C500",
                        "Yonge North Subway Extension",
                        "#F1C500",
                        "Line 2: Bloor-Danforth Subway",
                        "#16A753",
                        "Scarborough Subway Extension",
                        "#16A753",
                        "Line 3: Scarborough RT",
                        "#1F99D5",
                        "Line 4: Sheppard Subway",
                        "#B32078",
                        "Eglinton Crosstown LRT",
                        "#F87005",
                        "Eglinton Crosstown West Extension",
                        "#F87005",
                        "Eglinton East LRT",
                        "#F87005",
                        "Eglinton Crosstown West Extension - Airport Segment",
                        "#F87005",
                        "Finch West LRT",
                        "#888888",
                        "Ontario Line",
                        "#000000",
                        "#FFFFFF",
                    ],
                    "circle-stroke-width": 2,
                },
                //before: "transit-line-bold-ID",
            });
            // map libre is not really smart, you will have to create a symbol layer to label your circle layer
            map.addLayer({
                id: "transit-station-labels",
                type: "symbol",
                source: "transit_station",
                filter: ["==", "NAME", transitName],
                layout: {
                    "text-field": ["get", "LOCATION_N"], // Use the property for labeling
                    "text-size": 12,
                    "text-anchor": "left", // Base placement
                    "text-offset": [1, 1], // Adjust vertical offset
                    "text-justify": "center", // Align text within the box
                },
                paint: {
                    "text-color": "black",
                    "text-halo-color": "white", // Color of the halo
                    "text-halo-width": 5,
                    // Other paint properties for text appearance
                },
                before: "transit-station-ID",
            });
        });
        map.fitBounds([
            [-79.14904366238247, 43.87527014932047],
            [-79.70668327438583, 43.56196116510192],
        ]);
    });
</script>

<main>
    <div id="map" />
</main>

<style>
    main {
        overflow-y: hidden;
        max-width: 90%;
        max-height: 30%;
    }
    @media only screen and (max-width: 1258px) {
        #map {
            top: 50%;
        }
    }
    @media only screen and (max-width: 700px) {
        #map {
            max-width: 100%;
            padding-left: 0%;
        }
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
        height: 60vh;
        width: 100%;
        top: 0;
        position: relative;
        z-index: 2;
    }
</style>
