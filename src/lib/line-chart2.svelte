<script>
    import { scaleLinear } from "d3-scale";
    import jsondata from "../data/data.json";
    import "../assets/global-styles.css";
    import cdData from "../data/cityAverage.json";
  
    //export let data;
    export let variable96;
    export let variable21;
    export let colour;
    export let colour2;
    let maxHeight = 700;
   
    export let transitName;
  
    let width = 200;
    let height = 100;
  
    $: height = Math.min(width / 2.42, maxHeight) + 100;
  
    //filtre data.json to the selected transitName in page.svelte
    function filterDesignation(jsondata) {
        return jsondata["Transit Line"] === transitName;
    }
  
    console.log(transitName);
    var data = jsondata.filter(filterDesignation);
  
    // create a list of ID
    var pointList = data.map(function (obj) {
        return obj["Point ID"];
    });
    // find the max value of the selected 1996 and 2021 variable
    var yMax = data.map(function (obj) {
        var max = Math.max(obj[variable96], obj[variable21]);
        return max;
    });
    var varName = variable96.replace(" 96", "").replace("Weighted ", "");
  
    var max = Math.max.apply(Math, yMax);
  
    // round the numbers for creating yticks
    var digits = max.toExponential().split("e+");
    var newMax = Math.ceil(parseFloat(digits[0])) * 10 ** parseInt(digits[1]);
  
    
    // create yticks
    var yTicks = [];
    for (let i = 0; i <= newMax; i += interval) {
        yTicks.push(Math.round(i));
    }
  
    const xTicks = pointList;
  
    const padding = { top: 20, right: 20, bottom: 10, left: 15 };
  
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
        .range([3 * padding.left, width - padding.right]);
  
    $: yScale = scaleLinear()
        .domain([0, Math.max.apply(null, yTicks)])
        .range([height - padding.bottom, padding.top + 0.2 * height]); // added 0.2*height to accomodate station text label.
  
    $: innerWidth = width - (padding.left + padding.right);
    console.log(cdData[0][varName]);
  
    $: barWidth = Math.max(Math.min(innerWidth / xTicks.length, 25), 6);
  
    
  
    let mouse_x, mouse_y;
    const setMousePosition = function (event) {
        mouse_x = event.clientX;
        mouse_y = event.clientY;
    };
  
  </script>
  
  <div id="barchart" class="chart" bind:clientWidth={width}>
    <svg width={xTicks.length * barWidth} {height}>
        <!-- this is the station separation lines-->
        <g class="year-tick">
            {#if innerWidth > 1000}
                {#each data as point, i}
                    {#if point.Label === "Label" && i + 1 < data.length}
                        <line
                            class="year-grid"
                            x1={xScale(i) + barPadding}
                            y1={height - padding.bottom}
                            x2={xScale(i) + barPadding}
                            y2={height * 0.2}
                            stroke-width={1}
                            stroke="#fff"
                            stroke-dasharray="5 3"
                            opacity="0.5"
                        />
                        <circle
                            class="point"
                            r={innerWidth / 300}
                            cx={xScale(i) + barPadding}
                            cy={height * 0.22}
                            stroke-width="2px"
                            stroke="#FFFFFF"
                            fill="#000000"
                            on:mouseover={(event) => {
                                selected_datapoint = point;
                                selected_datapoint_i = i;
                                setMousePosition(event);
                            }}
                        />
                    {/if}
                    
                    <!--Special label position for the last tick-->
                    {#if point.Label === "Label" && i + 1 === data.length}
                        <line
                            class="year-grid"
                            x1={xScale(i) + barPadding + barWidth}
                            y1={height - padding.bottom}
                            x2={xScale(i) + barPadding + barWidth}
                            y2={height * 0.2}
                            stroke-width={1}
                            stroke="#fff"
                            stroke-dasharray="5 3"
                            opacity="0.5"
                        />
                        <circle
                            class="point"
                            r={innerWidth / 300}
                            cx={xScale(i) + barPadding + barWidth}
                            cy={height * 0.22}
                            stroke-width="2px"
                            stroke="#FFFFFF"
                            fill="#000000"
                            on:mouseover={(event) => {
                                selected_datapoint = point;
                                selected_datapoint_i = i;
                                setMousePosition(event);
                            }}
                        />
                    {/if}
                {/each}
            {/if}
            <!-- this is the station separation lines when windows is smaller-->
            {#if innerWidth <= 1000 && innerWidth >= 700}
                {#each data as point, i}
                    {#if point.Label === "Label" && point["Station ID"] % 2 === 0 && i + 1 < data.length}
                        <line
                            class="year-grid"
                            x1={xScale(i) + barPadding}
                            y1={height - padding.bottom}
                            x2={xScale(i) + barPadding}
                            y2={height * 0.2}
                            stroke-width={1}
                            stroke="#fff"
                            stroke-dasharray="5 3"
                            opacity="0.5"
                        />
                        <circle
                            class="point"
                            r={innerWidth / 300}
                            cx={xScale(i) + barPadding}
                            cy={height * 0.28}
                            stroke-width="2px"
                            stroke="#FFFFFF"
                            fill="#000000"
                            on:mouseover={(event) => {
                                selected_datapoint = point;
                                selected_datapoint_i = i;
                                setMousePosition(event);
                            }}
                        />
                    {/if}
                    <!--Special label position for the last tick-->
                    {#if point.Label === "Label" && point["Station ID"] % 2 === 0 && i + 1 === data.length}
                        <line
                            class="year-grid"
                            x1={xScale(i) + barPadding + barWidth}
                            y1={height - padding.bottom}
                            x2={xScale(i) + barPadding + barWidth}
                            y2={height * 0.2}
                            stroke-width={1}
                            stroke="#fff"
                            stroke-dasharray="5 3"
                            opacity="0.5"
                        />
                        <circle
                            class="point"
                            r={innerWidth / 300}
                            cx={xScale(i) + barPadding + barWidth}
                            cy={height * 0.22}
                            stroke-width="2px"
                            stroke="#FFFFFF"
                            fill="#000000"
                            on:mouseover={(event) => {
                                selected_datapoint = point;
                                selected_datapoint_i = i;
                                setMousePosition(event);
                            }}
                        />
                    {/if}
                {/each}
            {/if}
        </g>
        <!--Census Division Value Showing City Average-->
        <!--
        <g>
            <line
                x1={padding.left*4}
                y1={yScale(cdData[0][varName])}
                x2={xScale(data.length) + barWidth}
                y2={yScale(cdData[0][varName])}
                stroke={"grey"}
                stroke-width="1"
            />
            </g>
            -->
        <g>
            <line
                x1={padding.left * 4}
                y1={yScale(cdData[1][varName])}
                x2={xScale(data.length) + barWidth}
                y2={yScale(cdData[1][varName])}
                stroke={"white"}
                stroke-width="1"
            />
        </g>
  
        <!--  x axis labels  -->
        <g class = "average">
            <text 
                x={padding.left * 4}
                y={yScale(cdData[1][varName])}
                text-anchor="start"
            >
                {"2021 Average: "}{cdData[1][varName]}
            </text>
        </g>

        
        <g class="axis x-axis">
            {#each data as point, i}
                {#if innerWidth > 1000}
                    {#if point.Label === "Label" && i + 1 < data.length}
                        <g
                            class="stationtick"
                            transform="translate({xScale(i)},{height}) "
                        >
                            <text
                                x={height * -0.2}
                                y={xScale(i) + barPadding + innerWidth / 300}
                                text-anchor="start"
                            >
                                {point["Station Name"]}
                            </text>
                        </g>
                    {/if}
                    {#if point.Label === "Label" && i + 1 === data.length}
                        <g
                            class="stationtick"
                            transform="translate({xScale(i)},{height}) "
                        >
                            <text
                                x={height * -0.2}
                                y={xScale(i) +
                                    barPadding +
                                    barWidth +
                                    innerWidth / 300}
                                text-anchor="start"
                            >
                                {point["Station Name"]}
                            </text>
                        </g>
                    {/if}
                    <!--  x axis labels for smaller window size -->
                {:else if innerWidth <= 1000 && innerWidth >= 700}
                    <!-- if the inner window width <=800 show years only-->
                    {#if point.Label === "Label" && point["Station ID"] % 2 === 0 && i + 1 < data.length}
                        <g
                            class="stationtick"
                            transform="translate({xScale(i)},{height})"
                        >
                            <text
                                x={height * -0.25}
                                y={xScale(i) + barPadding + innerWidth / 300}
                                text-anchor="start"
                            >
                                {point["Station Name"]}
                            </text>
                        </g>
                    {/if}
                    {#if point.Label === "Label" && point["Station ID"] % 2 === 0 && i + 1 === data.length}
                        <g
                            class="stationtick"
                            transform="translate({xScale(i)},{height})"
                        >
                            <text
                                x={height * -0.25}
                                y={xScale(i) +
                                    barPadding +
                                    barWidth +
                                    innerWidth / 300}
                                text-anchor="start"
                            >
                                {point["Station Name"]}
                            </text>
                        </g>
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
  
        <!-- the lines and circles of the line chart  -->
  
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
                    />
  
                    <rect
                        class="barLight"
                        x={xScale(i) + barPadding}
                        y={yScale(
                            Math.max(point[variable21], point[variable96])
                        )}
                        width={barWidth - 2}
                        height={yScale(0) -
                            yScale(
                                Math.max(point[variable21], point[variable96])
                            )}
                        stroke={colour}
                        opacity="0.15"
                        on:mouseover={(event) => {
                            selected_datapoint = point;
                            setMousePosition(event);
                            selected_datapoint_i = i;
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
            {selected_datapoint["Station Name"].toString().toLocaleString() +
                " (" +
                selected_datapoint["Count"] +
                ")" +
                " "}: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"1996"}
            <span id="lightBlue"
                >{selected_datapoint[variable96].toLocaleString()}</span
            >
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"2021 "}
            <span id="lightGreen"
                >{selected_datapoint[variable21].toLocaleString()}</span
            >
        {/if}
    </p>
  </div>
  
  <style>
    .chart {
        width: 90%;
        max-width: 100%;
        min-width: 500px;
        margin: 0 auto;
        padding-top: 1%;
    }
    .average{
        font-size: 15px;
        fill: #FFFFFF;
    }
    @media only screen and (max-width: 300px) {
        .chart {
            width: 96%;
            max-width: 100%;
            min-width: 500px;
            margin: 0 auto;
            padding-top: 2%;
        }
        #hoverLabel p {
            color: var(--brandWhite);
            font-family: RobotoRegular;
            font-size: 10px;
            text-align: center;
        }
    }
    @media only screen and (max-width: 1258px) {
        .chart {
            width: 90%;
            max-width: 100%;
            min-width: 500px;
            margin: 0 auto;
            padding-top: 0%;
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
        padding: 10%;
    }
    /* controls the styling for all tick texts */
    .tick text {
        fill: var(--brandGray);
        text-anchor: start;
        font-size: 16px;
    }
  
    .tick.tick-0 line {
        stroke-dasharray: 0;
    }
  
    .x-axis .tick text {
        text-anchor: middle;
        font-size: 15px;
        text-align: left;
    }
  
    .x-label {
        text-anchor: middle;
        transform: translate(-10px, 0px) rotate(-45deg);
    }
  
    .x-label.tick text {
        font-size: 15px;
        fill: #000000;
    }
    .x-axis .stationtick {
        text-anchor: right;
        fill: var(--brandGray);
        font-size: 15px;
        text-align: right;
        transform: rotate(-90deg);
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