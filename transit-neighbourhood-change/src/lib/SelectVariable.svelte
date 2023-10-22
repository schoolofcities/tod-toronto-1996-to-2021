<script>
    import { selectedVariable } from "./stores.js";
    import "../assets/global.css";
    import { onMount } from "svelte";
    import { csvParse } from "d3-dsv";
    import data from "../routes/data/transit_buffer.json";
    let initialVariable;

    let dataDictionary = [];

    let dataDictionaryCommuting = [];
    let dataDictionaryCovid = [];
    let transit_lines = [];
    let dataDictionaryEmployment = [];
    let dataDictionaryHousing = [];
    let dataDictionaryIncome = [];
    let dataDictionaryPolitics = [];
    let dataDictionaryWeather = [];
    /*
    async function loadDataDictionary() {
        try {
            const response = await fetch("../variables_data_dictionary.csv");
            const csvData = await response.text();
            dataDictionary = csvParse(csvData);
        } catch (error) {
            console.error("Error loading CSV data:", error);
        }
    }

    onMount(() => {
        loadDataDictionary();
        initialVariable = $selectedVariable;
    });*/

    transit_lines = [
        "Yonge-University Subway",
        "Spadina Subway Extension",
        "Yonge North Subway Extension",
        "Bloor-Danforth Subway",
        "Scarborough Subway",
        "Scarborough RT",
        "Sheppard Subway",
        "Sheppard East",
        "Eglinton Crosstown LRT",
        "Finch West LRT",
        "Ontario Line",
    ];

    function handleChange(event) {
        const selectedValue = event.target.value;
        selectedVariable.set(selectedValue);
        
    }
</script>

<p>Select Variable:</p>
<select value={initialVariable} on:change={handleChange}>
    {#each transit_lines as v}
        <option value={v}>{v}</option>
    {/each}
</select>

<style>
    select {
        max-width: 600px;
        max-width: calc(100vw - 30px);
        padding: 5px;
        background-color: var(--brandGray90);
        border: 1px solid var(--brandDarkBlue);
        color: white;
    }

    select option {
        background-color: var(--brandGray90);
        color: white;
    }

    select:hover {
        cursor: pointer;
        background-color: black;
    }
</style>
