<script>
    import { scaleLinear } from "d3-scale";
    import jsondata from "../data/data.json";
    import "../assets/global-styles.css";

    //export let data;
    export let variable96;
    export let variable21;
    export let colour;
    export let colour2;
    export let maxHeight;
    export let transitName;

    let width = 200;
    let height = 60;

    $: height = Math.min(width / 2.42, maxHeight);

    // filtering data
    function filterDesignation(jsondata) {
        return jsondata.NAME === transitName;
    }

    var data = jsondata.filter(filterDesignation);

    // create a list of ID
    var pointList = data.map(function (obj) {
        return obj.ID;
    });

    // find the max value of the selected 1996 and 2021 variable
    var yMax = data.map(function (obj) {
        var max = Math.max(obj[variable96], obj[variable21]);
        return max;
    });

    var max = Math.max.apply(Math, yMax);

    // round the numbers for creating yticks
    var digits = max.toExponential().split("e+");
    var newMax = Math.ceil(parseFloat(digits[0])) * 10 ** parseInt(digits[1]);

    var interval = newMax / 10;
    // create yticks
    var yTicks = [];
    for (let i = 0; i <= newMax; i += interval) {
        yTicks.push(i);
    }

    const xTicks = pointList;
    const padding = { top: 20, right: 25, bottom: 35, left: 15 };

    function formatMobile(tick) {
        return "'" + tick.toString().slice(-2);
    }

    // converts thousands and million to K and M i.e. (1,000 ==> 1K , 1,000,000 ==> 1M)
    function thousandToK(tick) {
        var newtick;
        if (tick >= 1000 && tick < 1000000) {
            newtick = tick / 1000 + "K";
        } else if (tick > 1000000) {
            newtick = tick / 1000000 + "M";
        } else {
            newtick = tick;
        }
        return newtick;
    }
    $: xScale = scaleLinear()
        .domain([0, xTicks.length])
        .range([padding.left, width - padding.right]);

    $: yScale = scaleLinear()
        .domain([0, Math.max.apply(null, yTicks)])
        .range([height - padding.bottom, padding.top]);

    $: innerWidth = width - (padding.left + padding.right);

    $: barWidth = Math.max(Math.min(innerWidth / xTicks.length, 9), 6);

    let selected_datapoint = undefined;
    let selected_datapoint_i = undefined;

    let mouse_x, mouse_y;
    const setMousePosition = function (event) {
        mouse_x = event.clientX;
        mouse_y = event.clientY;
    };

    var barPadding = 10; // controls how much spacing the bars will be from the
</script>

<div id="barchart" class="chart" bind:clientWidth={width}>
    <svg width={xTicks.length * barWidth} {height}>
        <!-- this is the year separation lines-->
        <g class="year-tick">
            {#each data as point, i}
                {#if point.ID === 1 && i > 0}
                    <line
                        class="year-grid"
                        x1={xScale(i) + barPadding - innerWidth / 600}
                        y1={height - 3}
                        x2={xScale(i) + barPadding - innerWidth / 600}
                        y2={0}
                        stroke-width={1}
                        stroke="#fff"
                        stroke-dasharray="5 3"
                        opacity="0.5"
                    />
                {/if}
            {/each}
        </g>

        <!-- Second x axis, only appears when the inner window width > 800 -->
        <g class="axis x-axis">
            {#each data as point, i}
                {#if innerWidth > 500}
                    {#if point.ID === 1 || i == 0}
                        <g class="tick">
                            <text
                                x={xScale(i) +
                                    17 +
                                    barPadding -
                                    innerWidth / 600}
                                y={height - 5}
                                text-anchor="end"
                            />
                        </g>
                    {/if}
                {/if}
            {/each}
        </g>
        <!--  x axis - monthly-->
        <g class="axis x-axis">
            {#each data as point, i}
                {#if innerWidth > 1700}
                    <!-- if the inner window width > 800, show months as label-->
                    <g class="tick" transform="translate({xScale(i)},{height})">
                        <text x={barWidth / 2 + 9} y="-20">{point.ID}</text>
                    </g>
                {:else if innerWidth <= 1700}
                    <!-- if the inner window width <=800 show years only-->
                    {#if point.ID === 1 || i == 0}
                        <p></p>
                    {/if}
                {/if}
            {/each}
        </g>

        <!-- y axis -->
        <g class="axis y-axis">
            {#each yTicks as tick}
                <g
                    class="tick tick-{tick}"
                    transform="translate(0, {yScale(tick)})"
                >
                    <line x2="100%" />
                    <text y="-4">{thousandToK(tick)} </text>
                </g>
            {/each}
        </g>

        <g>
            {#each data as point, i}
                {#if i > 0 && point[variable96] !== null && data[i - 1][variable96] !== null}
                    <line
                        x1={xScale(i - 1) + barPadding + barWidth / 2 - 1}
                        y1={yScale(data[i - 1][variable96])}
                        x2={xScale(i) + barPadding + barWidth / 2 - 1}
                        y2={yScale(point[variable96])}
                        stroke={colour}
                        stroke-width="2"
                    />
                {/if}
                {#if i > 0 && point[variable21] !== null && data[i - 1][variable21] !== null}
                    <line
                        x1={xScale(i - 1) + barPadding + barWidth / 2 - 1}
                        y1={yScale(data[i - 1][variable21])}
                        x2={xScale(i) + barPadding + barWidth / 2 - 1}
                        y2={yScale(point[variable21])}
                        stroke={colour2}
                        stroke-width="2"
                    />
                {/if}

                {#if point[variable96] !== null}
                    <circle
                        class="point"
                        r={innerWidth / 400}
                        cx={xScale(i) + barPadding + barWidth / 2 - 1}
                        cy={yScale(point[variable96])}
                        fill={colour}
                        on:mouseover={(event) => {
                            selected_datapoint = point;
                            selected_datapoint_i = i;
                            setMousePosition(event);
                        }}
                        on:mouseout={() => {
                            selected_datapoint = undefined;
                        }}
                    />
                    <circle
                        class="point"
                        r={innerWidth / 400}
                        cx={xScale(i) + barPadding + barWidth / 2 - 1}
                        cy={yScale(point[variable21])}
                        fill={colour2}
                        on:mouseover={(event) => {
                            selected_datapoint = point;
                            selected_datapoint_i = i;
                            setMousePosition(event);
                        }}
                        on:mouseout={() => {
                            selected_datapoint = undefined;
                        }}
                    />

                    <rect
                        class="barLight"
                        x={xScale(i) + barPadding}
                        y={yScale(point[variable96])}
                        width={barWidth - 2}
                        height={yScale(0) - yScale(point[variable96])}
                        stroke={colour}
                        opacity="0.15"
                        on:mouseover={(event) => {
                            selected_datapoint = point;
                            setMousePosition(event);
                            selected_datapoint_i = i;
                        }}
                        on:mouseout={() => {
                            selected_datapoint = undefined;
                        }}
                    />
                    <rect
                        class="barLight"
                        x={xScale(i) + barPadding}
                        y={yScale(point[variable21])}
                        width={barWidth - 2}
                        height={yScale(0) - yScale(point[variable21])}
                        stroke={colour}
                        opacity="0.15"
                        on:mouseover={(event) => {
                            selected_datapoint = point;
                            setMousePosition(event);
                            selected_datapoint_i = i;
                        }}
                        on:mouseout={() => {
                            selected_datapoint = undefined;
                        }}
                    />
                {/if}
            {/each}
        </g>
    </svg>
</div>

<div id="hoverLabel">
    <p>
        {#if selected_datapoint != undefined}
            <br />
            {selected_datapoint.Station.toString().toLocaleString() +
                "(" +
                selected_datapoint.ID +
                ")" +
                " "}:

            <br />{"2006"}
            <span id="lightBlue"
                >{selected_datapoint[variable96].toLocaleString()}</span
            >
            <br />{"2021 "}
            <span id="lightGreen"
                >{selected_datapoint[variable21].toLocaleString()}</span
            >
        {/if}
    </p>
</div>

<style>
    .chart {
        width: 80%;
        max-width: 100%;
        min-width: 500px;
        margin: 0 auto;
        padding-top: 5%;
    }
    @media only screen and (max-width: 300px) {
        .chart {
            width: 100%;
            max-width: 100%;
            min-width: 500px;
            margin: 0 auto;
            padding-top: 5%;
        }
        #hoverLabel p {
            color: var(--brandWhite);
            font-family: RobotoRegular;
            font-size: 10px;
            text-align: center;
        }
    }

    #hoverLabel {
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #hoverLabel p {
        color: var(--brandWhite);
        font-family: RobotoRegular;
        font-size: 15px;
        text-align: center;
    }

    #lightBlue {
        color: var(--brandLightBlue);
    }

    #lightGreen {
        color: var(--brandLightGreen);
    }

    svg {
        position: relative;
        width: 100%;
    }

    .tick {
        font-family: RobotoRegular;
        font-size: 0.725em;
        font-weight: 200;
    }

    .tick line {
        stroke: var(--brandGray);
        stroke-width: 1px;
        opacity: 0.1;
    }

    .tick text {
        fill: var(--brandGray);
        text-anchor: start;
        font-size: 12px;
    }

    .tick.tick-0 line {
        stroke-dasharray: 0;
    }

    .x-axis .tick text {
        text-anchor: middle;
        font-size: 12px;
        text-align: right;
    }

    .x-label {
        text-anchor: middle;
        transform: translate(-10px, 0px) rotate(-90deg);
    }

    .x-label.tick text {
        font-size: 15px; /* Adjust the font size as desired */
        fill: #000000; /* Adjust the font color as desired */
    }

    .bar {
        stroke: var(--brandDarkGreen);
        stroke-width: 1px;
        stroke-opacity: 1;
        fill: var(--brandWhite);
        cursor: pointer;
    }

    .bar:hover {
        fill: var(--brandLightBlue);
        opacity: 1;
    }

    .barLight {
        stroke: var(--brandDarkGreen);
        stroke-width: 1px;
        stroke-opacity: 1;
        fill: var(--brandWhite);
    }

    .barLight:hover {
        opacity: 0.4;
        cursor: pointer;
    }

    .point {
        cursor: pointer;
    }

    .point:hover {
        fill: var(--brandLightBlue);
        opacity: 1;
    }

    .tip {
        stroke: var(--brandDarkGreen);
        stroke-width: 1px;
        fill: var(--brandYellow);
    }

    .year-tick {
        stroke-width: 2px;
        z-index: 6;
    }
</style>
