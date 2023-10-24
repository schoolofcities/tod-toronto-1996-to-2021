<script>
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    //import transitPoint from "../data/transit-lines.geojson"
    //import transitLines from "../data/transit-point.geojson"
    import transitStation from "../data/transit-station.geojson.json"
    //import { featureGroup } from 'leaflet';

    //console.log(transitLines)

    let mapElement;
    let map;

    onMount(async () => {
        if(browser) {
            const leaflet = await import('leaflet');

            map = leaflet.map(mapElement).setView([43.67846737413526, -79.40948021185388], 13);

            leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            leaflet.geoJSON(transitStation,{
                style: function(feature) {
                    switch (feature.properties.NAME) {
                        case "Yonge-University Subway"         : return {color: "#ff0000"};
                        case "Spadina Subway Extension"        : return {color: "#ff0000"};
                        case "Yonge North Subway Extension"    : return {color: "#ff0000"};
                        case "Bloor-Danforth Subway"           : return {color: "#ff0000"};
                        case "Scarborough Subway"              : return {color: "#ff0000"};
                        case "Scarborough RT"                  : return {color: "#ff0000"};
                        case "Sheppard Subway"                 : return {color: "#ff0000"};
                        case "Sheppard East"                   : return {color: "#ff0000"};
                        case "Eglinton Crosstown LRT"          : return {color: "#ff0000"};
                        case "Finch West LRT"                  : return {color: "#ff0000"};
                        case "Ontario Line"                    : return {color: "#ff0000"};
                    }
                }
            }).addTo(map);
        }
    });

    onDestroy(async () => {
        if(map) {
            console.log('Unloading Leaflet map.');
            map.remove();
        }
    });
</script>


<main>
    <div bind:this={mapElement}></div>
</main>

<style>
    @import 'leaflet/dist/leaflet.css';
    main div {
        height: 800px;
    }
</style>