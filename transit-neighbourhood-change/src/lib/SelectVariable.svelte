<script>
    //import { selectedVariable } from "./stores.js";
    import "../assets/global-styles.css";
    import { onMount } from "svelte";
    import { csvParse } from "d3-dsv";
    //import data from "../routes/data/transit_buffer.json";

    let initialVariable;
    let dataDictionary = [];
    let dataDictionaryCommuting = [];
    let dataDictionaryCovid = [];
    export let transit_lines;
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

    function handleChange(event) {
        const selectedValue = event.target.value;
        console.log(selectedValue)
        //selectedVariable.set(selectedValue);
        
    }

    //console.log(selectedValue)
</script>

<p>Select Variable:</p>
<select value={initialVariable} on:change={handleChange}>
    {#each transit_lines as v}
        <option value={v}>{v}</option>
    {/each}
</select>

<style>
    
</style>
