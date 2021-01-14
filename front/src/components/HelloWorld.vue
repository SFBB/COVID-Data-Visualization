<template>
<div class="flexbox">
    <!-- <div class="hello" ref="chartdiv">
    </div> -->

  <div id="chartdiv"></div>



  <!-- Modal -->
  <transition name="fade">
    <div class="modal" v-if="show">
      <div class="modal__backdrop" v-on:click="closeChart()"/>

      <div class="modal__dialog">
        <div class="modal__header">
          <h1 id="keys_title">{{showing}}</h1>
          <button type="button" class="modal__close" v-on:click="closeChart()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512">
              <path
                fill="currentColor"
                d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"
              ></path>
            </svg>
          </button>
        </div>

        <div class="modal__body">
          <div id="DetailsChart"></div>
        </div>

        <div class="modal__footer">
          <select id="keys" v-on:change="changeChart()">
            <option v-for="(key) in keys" :key="key" :value="key">{{key}}</option>
          </select>
          <!-- <button v-on:click="closeChart()">Cancel</button>
          <button v-on:click="closeChart()">Save</button> -->
        </div>
        </div>
      </div>
  </transition>





<!-- <div id="chartdiv"></div> -->
  <button class="btn btn-info" v-on:click="dataShown(true)">Filter</button>
  <button class="btn btn-danger" v-on:click="clear()">Clear</button>
  <button class="btn btn-warning" v-on:click="showchart()">Show Chart</button>



<!-- <div id="buttons"></div> -->
</div>
</template>

<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_worldLow from "@amcharts/amcharts4-geodata/worldLow";
// import am4geodata_data_countries2 from "@amcharts/amcharts4-geodata/data/countries2";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
// import covid_total_timeline from "./json/total_timeline.json";
// import covid_world_timeline from "./json/world_timeline.json";
// import $ from 'jquery';
// import * as dt from 'datatables.net';
import axios from "axios";
import { fitNumberRelative } from '@amcharts/amcharts4/.internal/core/utils/Utils';


// console.log(JSON.parse(JSON.stringify(covid_world_timeline[0].list)));
// console.log(dt);

// var dt = require( 'datatables.net' )();
// import * as covid_t/tal_timeline from "./js/world_timeline"

am4core.useTheme(am4themes_animated);



export default {
  name: 'HelloWorld',
  data(){
    return {
      MapData: [1, 2, 3],
      Shown: {},
      records: {},
      realdata: null,
      bubbleSeriess: null,
      showing: "累计确诊",
      // keysshowing: {"新增确诊": true},
      show: false
    }
  },
  mounted(){
    var countryColor = am4core.color("#3b3b3b");
    var countryStrokeColor = am4core.color("#000000");
    // var buttonStrokeColor = am4core.color("#ffffff");
    var countryHoverColor = am4core.color("#1b1b1b");
    var activeCountryColor = am4core.color("#0f0f0f");


    // get data
    // var mapData;
    var bubbleSeries;
    var polygonSeries;

    axios.get("http://127.0.0.1:5000/api/countries_")
      .then( function(Response) {
        var mapData = Response.data.countries;
        this.realdata = [...mapData];
        mapData.forEach(function(cou){
          this.Shown[cou.id] = false;
        }.bind(this));
        // console.log(this.MapData);
        this.MapData = [...Response.data.countries];
        // console.log(mapData);

        var container  = am4core.create("chartdiv", am4core.Container);
        // container.wheelable = false;
        container.width = am4core.percent(100);
        container.height = am4core.percent(100);
        container.tooltip = new am4core.Tooltip();
        container.tooltip.background.fill = am4core.color("#000000");
        container.tooltip.background.stroke = am4core.color("#ff8726");
        container.tooltip.fontSize = "0.9em";
        container.tooltip.getFillFromObject = false;
        container.tooltip.getStrokeFromObject = false;

        var map = container.createChild(am4maps.MapChart);
        map.chartContainer.wheelable = false;
        map.zoomControl = new am4maps.ZoomControl();
        // map.height = am4core.percent(100);
        map.geodata = am4geodata_worldLow;
        // am4maps.projections.Mercator
        map.projection = new am4maps.projections.Mercator();
        map.panBehavior = "move";
        polygonSeries = map.series.push(new am4maps.MapPolygonSeries());
        polygonSeries.useGeodata = true
        polygonSeries.mapPolygons.template.events.on("hit", function(ev) {
          // map.zoomToMapObject(ev.target)
          console.log(ev.target.isActive);
          // if(ev.target.isActive)
          this.Shown[ev.target.dataItem.dataContext.id] = !ev.target.isActive;
          this.records[ev.target.dataItem.dataContext.id] = ev.target;
          // console.log(this.Shown);
          // console.log(ev.target.isActive);
          // ev.target.isActive = !ev.target.isActive;
          // console.log(ev.target.dataItem.dataContext.id);
        }.bind(this));
        map.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 0.05;
        map.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#ffffff");
        map.backgroundSeries.hidden = true;

        var button = map.chartContainer.createChild(am4core.Button);
        button.label.text = "...";
        button.padding(5, 5, 5, 5);
        button.width = 20;
        button.align = "right";
        button.marginRight = 15;
        button.events.on("hit", function() {
          map.goHome();
        });

        polygonSeries.dataFields.id = "id";
        polygonSeries.dataFields.value = "累计确诊";
        polygonSeries.interpolationDuration = 0;

        polygonSeries.exclude = ["AQ"]; // Antarctica is excluded in non-globe projection
        polygonSeries.useGeodata = true;
        polygonSeries.nonScalingStroke = true;
        polygonSeries.strokeWidth = 0.5;
        // this helps to place bubbles in the visual middle of the area
        polygonSeries.calculateVisualCenter = true;
        polygonSeries.data = JSON.parse(JSON.stringify(mapData));

        var polygonTemplate = polygonSeries.mapPolygons.template;
        polygonTemplate.fill = countryColor;
        polygonTemplate.fillOpacity = 1
        polygonTemplate.stroke = countryStrokeColor;
        polygonTemplate.strokeOpacity = 0.15
        polygonTemplate.setStateOnChildren = true;
        polygonTemplate.tooltipPosition = "fixed";

        // polygonTemplate.events.on("hit", handleCountryHit);
        // polygonTemplate.events.on("over", handleCountryOver);
        // polygonTemplate.events.on("out", handleCountryOut);


        polygonSeries.heatRules.push({
          "target": polygonTemplate,
          "property": "fill",
          "min": countryColor,
          "max": countryColor,
          "dataField": "value"
        })
        map.deltaLongitude = -8;

        // polygon states
        var polygonHoverState = polygonTemplate.states.create("hover");
        polygonHoverState.transitionDuration = 1400;
        polygonHoverState.properties.fill = map.colors.getIndex(25);
        // polygonHoverState.properties.fill = map.colors.getIndex(20);

        var activeState = polygonTemplate.states.create("active");
        activeState.properties.fill = map.colors.getIndex(30);

        polygonTemplate.events.on("hit", function(ev) {
          ev.target.isActive = !ev.target.isActive;
        })


        polygonSeries.heatRules.push({
          property: "fill",
          target: polygonSeries.mapPolygons.template,
          min: map.colors.getIndex(8).brighten(2),
          max: map.colors.getIndex(8).brighten(-10)
        });

        // var polygonActiveState = polygonTemplate.states.create("active")
        // polygonActiveState.properties.fill = activeCountryColor;

        // Bubble series
        bubbleSeries = map.series.push(new am4maps.MapImageSeries());
        this.bubbleSeriess = bubbleSeries;
        bubbleSeries.data = JSON.parse(JSON.stringify(mapData));

        bubbleSeries.dataFields.value = "累计确诊";
        bubbleSeries.dataFields.id = "id";

        // adjust tooltip
        bubbleSeries.tooltip.animationDuration = 0;
        bubbleSeries.tooltip.showInViewport = false;
        bubbleSeries.tooltip.background.fillOpacity = 0.2;
        bubbleSeries.tooltip.getStrokeFromObject = true;
        bubbleSeries.tooltip.getFillFromObject = false;
        bubbleSeries.tooltip.background.fillOpacity = 0.2;
        bubbleSeries.tooltip.background.fill = am4core.color("#000000");

        var imageTemplate = bubbleSeries.mapImages.template;
        // if you want bubbles to become bigger when zoomed, set this to false
        imageTemplate.nonScaling = true;
        imageTemplate.strokeOpacity = 0;
        imageTemplate.fillOpacity = 0.55;
        imageTemplate.tooltipText = "{name}: [bold]{value}[/]";
        imageTemplate.applyOnClones = true;

        // imageTemplate.events.on("over", handleImageOver);
        // imageTemplate.events.on("out", handleImageOut);
        // imageTemplate.events.on("hit", handleImageHit);

        // this is needed for the tooltip to point to the top of the circle instead of the middle
        imageTemplate.adapter.add("tooltipY", function(tooltipY, target) {
          return -target.children.getIndex(0).radius;
        })

        // When hovered, circles become non-opaque  
        var imageHoverState = imageTemplate.states.create("hover");
        imageHoverState.properties.fillOpacity = 1;
        imageHoverState.properties.fill = map.colors.getIndex(45);

        // add circle inside the image
        var circle = imageTemplate.createChild(am4core.Circle);
        // this makes the circle to pulsate a bit when showing it
        circle.hiddenState.properties.scale = 0.0001;
        circle.hiddenState.transitionDuration = 2000;
        circle.defaultState.transitionDuration = 2000;
        circle.defaultState.transitionEasing = am4core.ease.elasticOut;
        // later we set fill color on template (when changing what type of data the map should show) and all the clones get the color because of this
        circle.applyOnClones = true;

        // heat rule makes the bubbles to be of a different width. Adjust min/max for smaller/bigger radius of a bubble
        bubbleSeries.heatRules.push({
          "target": circle,
          "property": "radius",
          "min": 3,
          "max": 30,
          "dataField": "value"
        })

        // when data items validated, hide 0 value bubbles (because min size is set)
        bubbleSeries.events.on("dataitemsvalidated", function() {
          bubbleSeries.dataItems.each((dataItem) => {
            var mapImage = dataItem.mapImage;
            var circle = mapImage.children.getIndex(0);
            if (mapImage.dataItem.value == 0) {
              circle.hide(0);
            }
            else if (circle.isHidden || circle.isHiding) {
              circle.show();
            }
          })
        })

        // this places bubbles at the visual center of a country
        imageTemplate.adapter.add("latitude", function(latitude, target) {
          var polygon = polygonSeries.getPolygonById(target.dataItem.id);
          if (polygon) {
            target.disabled = false;
            return polygon.visualLatitude;
          }
          else {
            target.disabled = true;
          }
          return latitude;
        })

        imageTemplate.adapter.add("longitude", function(longitude, target) {
          var polygon = polygonSeries.getPolygonById(target.dataItem.id);
          if (polygon) {
            target.disabled = false;
            return polygon.visualLongitude;
          }
          else {
            target.disabled = true;
          }
          return longitude;
        })

    }.bind(this));

    // var button = am4core.create("buttons", am4core.PlayButton);
    // button.events.on("toggled", function(event) {
    //   if (event.target.isActive) {
    //     console.log("asda");
    //     axios.get("http://127.0.0.1:5000/api/countries_2020")
    //       .then((Response) => {
    //           bubbleSeries.dataItems.each(function(dataItem) {
    //             console.log(dataItem.dataContext.name, dataItem.dataContext.累计确诊);
    //             dataItem.dataContext.累计确诊 = 0;
    //             // dataItem.dataContext.deaths = 0;
    //             // dataItem.dataContext.recovered = 0;
    //             // dataItem.dataContext.active = 0;
    //         })
    //       });
    //   } else {
    //     console.log("526566");
    //   }
    // });

    this.$root.$on('shown', function(Shown) {
      
      // bubbleSeries.data = temp;
      (async function() {
        const dogs = await redraw(Shown, this.MapData);
        // console.log(dogs)
      }.bind(this))()
      
      // console.log("Received!");
      // console.log(temp);

    }.bind(this));

    this.$root.$on('datashowing', function(data_to_show) {
      
      // console.log(data_to_show);
      this.showing = data_to_show;
      bubbleSeries.dataFields.value = data_to_show;
      polygonSeries.dataFields.value = data_to_show;
      this.MapData = [...this.realdata];
      polygonSeries.data = JSON.parse(JSON.stringify(this.MapData));
      bubbleSeries.data = JSON.parse(JSON.stringify(this.MapData));
      // // bubbleSeries.data = temp;
      // (async function() {
      //   const dogs = await redraw(Shown, this.MapData);
      //   console.log(dogs)
      // }.bind(this))()
      
      // console.log("Received!");
      // // console.log(temp);

    }.bind(this));


    this.$root.$on('date_updated', function(new_data) {
      console.log("sadasd!!!");
      // console.log(new_data);
      this.realdata = [...new_data];
      polygonSeries.data = JSON.parse(JSON.stringify(new_data));
      bubbleSeries.data = JSON.parse(JSON.stringify(new_data));
      this.MapData = new_data;
    }.bind(this));

    async function redraw(Shown, data){
      // console.log(Object.keys(Shown).length);
      // console.log(data);
      var temp = [...data];
      data.forEach(function(cou, ind){
        if(!Shown[cou.id]){
          // console.log(cou.id);
          if(temp.indexOf(cou)  > -1)
            temp.splice(temp.indexOf(cou), 1);
        }
      });
      this.realdata = [...temp];
      bubbleSeries.data = temp;
      // func("Done!");
      return "Done!";
    }

  },

  methods: {
    "get_data": function get_data(type, func){
      axios.get("http://127.0.0.1:5000/api/countries_")
        .then((Response) => {
          // var mapData = Response.data.countries;
          // console.log(Response.data);
          func(Response.data.countries);
          // this.MapData = Response.data.countries;
        });
    },
    "test": function test(type){
      return type;
    },
    "dataShown": function dataShown(condition) {
      // console.log(this.Shown);
      var from = document.getElementsByClassName("amcharts-range-selector-from-input")[0].value;
      var to = document.getElementsByClassName("amcharts-range-selector-to-input")[0].value;
      // console.log(from+to);
      var temp = [...this.realdata];
      this.realdata.forEach(function(cou, ind){
        if(!this.Shown[cou.id] && condition){
          // console.log(cou.id);
          if(temp.indexOf(cou)  > -1)
            temp.splice(temp.indexOf(cou), 1);
        }
        if(this.records[cou.id])
          this.records[cou.id].isActive = this.Shown[cou.id];
      }.bind(this));
      // this.realdata = [...temp];
      // console.log(temp.length);
      this.bubbleSeriess.data = JSON.parse(JSON.stringify(temp));
      this.$root.$emit('filter', this.Shown);
      // axios.get("http://127.0.0.1:5000/api/countries_")
      //   .then( function(Response) {
      //   });
    },
    "clear": function clear() {
      // console.log(this.realdata);
      // console.log(this.Shown);
      this.realdata.forEach(function(cou){
        // console.log(cou.id);
        this.Shown[cou.id] = false;
      }.bind(this));
      this.dataShown(false);
      this.$root.$emit('clear');
    },
    "showchart": function showchart() {
      
      // console.log("Show Chart!");
      var countries = {};
      var from = document.getElementsByClassName("amcharts-range-selector-from-input")[0].value;
      var to = document.getElementsByClassName("amcharts-range-selector-to-input")[0].value;
      Object.keys(this.Shown).forEach(function(cou){
        if(this.Shown[cou]){
          countries[cou] = [];
        }
      }.bind(this));
      // console.log(countries);
      var couL = "";
       Object.keys(countries).forEach(function(cou){
         couL += cou+",";
      });
      couL = couL.slice(0, couL.length-1);
      // console.log(couL);
      var showingg = this.showing;
      if(couL!="")
      {
        this.show = true;
        axios.get("http://127.0.0.1:5000/api/countriesL?from="+from+"&to="+to+"&countries="+couL+"&type="+this.showing)
          .then( function(Response) {
            // console.log(Response.data.countries);

            // var count = 1;
            // var length = countries.length;
            // var merged;
            // var data = [...Response.data.countries[Object.keys(Response.data.countries)[0]]];
            var data = [];
            // var couu = ;
            Response.data.countries[Object.keys(Response.data.countries)[0]].forEach(function(cou, index){
              var temp = {};
              temp.date = cou.date;
              temp[Object.keys(Response.data.countries)[0]] = cou[showingg];
              data.push(temp)
            });
            for(var i=1; i<Object.keys(Response.data.countries).length; i++){
              var values = Response.data.countries[Object.keys(Response.data.countries)[i]];
              // console.log(values);
              var indexes = values.map(obj => obj.date);
              data = data.map(obj => {
                var index = indexes.indexOf(obj.date);
                var cou = Object.keys(Response.data.countries)[i];
                // var b = {: index > -1? values[index].新增确诊 : obj.新增确诊};
                // console.log(obj);
                var temp = {};
                temp[Object.keys(Response.data.countries)[i]] = index > -1? values[index][showingg] : obj[showingg];
                return Object.assign({}, obj, temp);
              });
            }

            // console.log(data);



                  var chart = am4core.create("DetailsChart", am4charts.XYChart);

                  // Add data
                  chart.data = data;

                  // Create axes
                  var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
                  categoryAxis.renderer.grid.template.location = 0;
                  //categoryAxis.renderer.minGridDistance = 30;

                  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

                  // Create series
                  function createSeries(field, name) {
                    var series = chart.series.push(new am4charts.LineSeries());
                    series.dataFields.valueY = field;
                    series.dataFields.dateX = "date";
                    series.name = name;
                    series.tooltipText = "{dateX}: [b]{valueY}[/]";
                    series.strokeWidth = 2;
                    
                  var bullet = series.bullets.push(new am4charts.CircleBullet());
                  bullet.events.on("hit", function(ev) {
                    alert("Clicked on " + ev.target.dataItem.dateX + ": " + ev.target.dataItem.valueY);
                  });
                  }

                  var keyss = Object.keys(data[0]);
                  for(i=1; i<keyss.length; i++){
                    createSeries(keyss[i], keyss[i]);

                  }
                  // createSeries("value2", "Series #2");
                  // createSeries("value3", "Series #3");

                  chart.legend = new am4charts.Legend();
                  chart.cursor = new am4charts.XYCursor();
          });
      }
      else
        alert("Please select at least one country!");
      // cou = [...countries];
      // cou.forEach(function(cc, index){

      // });
    },
    "closeChart": function closeChart() {
      this.show = false;
    },
    "changeChart": function changeChart() {
      // console.log("Change!");
      // console.log(document.getElementById("keys").value);
      var showing = document.getElementById("keys").value;
      document.getElementById("keys_title").innerText = document.getElementById("keys").value;
      var countries = {};
      var from = document.getElementsByClassName("amcharts-range-selector-from-input")[0].value;
      var to = document.getElementsByClassName("amcharts-range-selector-to-input")[0].value;
      Object.keys(this.Shown).forEach(function(cou){
        if(this.Shown[cou]){
          countries[cou] = [];
        }
      }.bind(this));
      // console.log(countries);
      var couL = "";
       Object.keys(countries).forEach(function(cou){
        couL += cou+",";
      });
      couL = couL.slice(0, couL.length-1);
      // console.log(couL);
      var showingg = showing;
      if(couL!="")
        axios.get("http://127.0.0.1:5000/api/countriesL?from="+from+"&to="+to+"&countries="+couL+"&type="+showing)
          .then( function(Response) {
            // console.log(Response.data.countries);

            // var count = 1;
            // var length = countries.length;
            // var merged;
            // var data = [...Response.data.countries[Object.keys(Response.data.countries)[0]]];
            var data = [];
            // var couu = ;
            Response.data.countries[Object.keys(Response.data.countries)[0]].forEach(function(cou, index){
              var temp = {};
              temp.date = cou.date;
              temp[Object.keys(Response.data.countries)[0]] = cou[showingg];
              data.push(temp)
            });
            for(var i=1; i<Object.keys(Response.data.countries).length; i++){
              var values = Response.data.countries[Object.keys(Response.data.countries)[i]];
              // console.log(values);
              var indexes = values.map(obj => obj.date);
              data = data.map(obj => {
                var index = indexes.indexOf(obj.date);
                var cou = Object.keys(Response.data.countries)[i];
                // var b = {: index > -1? values[index].新增确诊 : obj.新增确诊};
                // console.log(obj);
                var temp = {};
                temp[Object.keys(Response.data.countries)[i]] = index > -1? values[index][showingg] : obj[showingg];
                return Object.assign({}, obj, temp);
              });
            }

            // console.log(data);



                  var chart = am4core.create("DetailsChart", am4charts.XYChart);

                  // Add data
                  chart.data = data;

                  // Create axes
                  var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
                  categoryAxis.renderer.grid.template.location = 0;
                  //categoryAxis.renderer.minGridDistance = 30;

                  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

                  // Create series
                  function createSeries(field, name) {
                    var series = chart.series.push(new am4charts.LineSeries());
                    series.dataFields.valueY = field;
                    series.dataFields.dateX = "date";
                    series.name = name;
                    series.tooltipText = "{dateX}: [b]{valueY}[/]";
                    series.strokeWidth = 2;
                    
                  var bullet = series.bullets.push(new am4charts.CircleBullet());
                  bullet.events.on("hit", function(ev) {
                    alert("Clicked on " + ev.target.dataItem.dateX + ": " + ev.target.dataItem.valueY);
                  });
                  }

                  var keyss = Object.keys(data[0]);
                  for(i=1; i<keyss.length; i++){
                    createSeries(keyss[i], keyss[i]);

                  }
                  // createSeries("value2", "Series #2");
                  // createSeries("value3", "Series #3");

                  chart.legend = new am4charts.Legend();
                  chart.cursor = new am4charts.XYCursor();
          });
    }
  },

  computed: {
    "get_MapData": function get_MapData(){
      // console.log(this.MapData);
      return this.MapData;
    },
    "keys": function keys() {
      var result = ["新增确诊", "新增死亡", "重症病例", "累计确诊", "累计治愈", "仍在治疗", "累计死亡"];
      result.splice(result.indexOf(this.showing), 1);
      result.unshift(this.showing);
      return result;
    }
  },

  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
}



</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
#chartdiv {
  width: 80%;
  height: 500px;
}
table {
  font-family: 'Open Sans', sans-serif;
  width: 750px;
  border-collapse: collapse;
  border: 3px solid #44475C;
  margin: 10px 10px 0 10px;
}

table th {
  text-transform: uppercase;
  text-align: left;
  background: #44475C;
  color: #FFF;
  cursor: pointer;
  padding: 8px;
  min-width: 30px;
}
table th:hover {
        background: #717699;
      }
table td {
  text-align: left;
  padding: 8px;
  border-right: 2px solid #7D82A8;
}
table td:last-child {
  border-right: none;
}
table tbody tr:nth-child(2n) td {
  background: #D4D8F9;
}

table {
  font-family: 'Open Sans', sans-serif;
  width: 750px;
  border-collapse: collapse;
  border: 3px solid #44475C;
  margin: 10px 10px 0 10px;
}

table th {
  text-transform: uppercase;
  text-align: left;
  background: #44475C;
  color: #FFF;
  cursor: pointer;
  padding: 8px;
  min-width: 30px;
}
table th:hover {
        background: #717699;
      }
table td {
  text-align: left;
  padding: 8px;
  border-right: 2px solid #7D82A8;
}
table td:last-child {
  border-right: none;
}
table tbody tr:nth-child(2n) td {
  background: #D4D8F9;
}

.pagination {
  font-family: 'Open Sans', sans-serif;
  text-align: right;
  width: 750px;
  padding: 8px;
}

.arrow_down {
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB8AAAAaCAYAAABPY4eKAAAAAXNSR0IArs4c6QAAAvlJREFUSA29Vk1PGlEUHQaiiewslpUJiyYs2yb9AyRuJGm7c0VJoFXSX9A0sSZN04ULF12YEBQDhMCuSZOm1FhTiLY2Rky0QPlQBLRUsICoIN/0PCsGyox26NC3eTNn3r3n3TvnvvsE1PkwGo3yUqkkEQqFgw2Mz7lWqwng7ztN06mxsTEv8U0Aam5u7r5EInkplUol/f391wAJCc7nEAgE9Uwmkzo4OPiJMa1Wq6cFs7Ozt0H6RqlUDmJXfPIx+qrX69Ti4mIyHA5r6Wq1egND+j+IyW6QAUoul18XiUTDNHaSyGazKcZtdgk8wqhUKh9o/OMvsVgsfHJy0iWqVrcQNRUMBnd6enqc9MjISAmRP3e73T9al3XnbWNjIw2+KY1Gc3imsNHR0YV4PP5+d3e32h3K316TySQFoX2WyWR2glzIO5fLTSD6IElLNwbqnFpbWyO/96lCoai0cZjN5kfYQAYi5H34fL6cxWIZbya9iJyAhULBHAqFVlMpfsV/fHxMeb3er+Vy+VUzeduzwWC45XA4dlD/vEXvdDrj8DvURsYEWK3WF4FA4JQP9mg0WrHZbEYmnpa0NxYgPVObm5teiLABdTQT8a6vrwdRWhOcHMzMzCiXlpb2/yV6qDttMpkeshEzRk4Wo/bfoe4X9vb2amzGl+HoXNT29vZqsVi0sK1jJScG+Xx+HGkL4Tew2TPi5zUdQQt9otPpuBk3e0TaHmMDh1zS7/f780S0zX6Yni+NnBj09fUZUfvudDrNZN+GkQbl8Xi8RLRtHzsB9Hr9nfn5+SjSeWUCXC7XPq5kw53wsNogjZNohYXL2EljstvtrAL70/mVaW8Y4OidRO1/gwgbUMvcqGmcDc9aPvD1gnTeQ+0nmaInokRj0nHh+uvIiVOtVvt2a2vLv7Ky0tL3cRTXIcpPAwMDpq6R4/JXE4vFQ5FI5CN+QTaRSFCYc8vLy1l0rge4ARe5kJ/d27kYkLXoy2Jo4C7K8CZOsEBvb+9rlUp1xNXPL7v3IDwxvPD6AAAAAElFTkSuQmCC')
}
.arrow_up {
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAaCAYAAACgoey0AAAAAXNSR0IArs4c6QAAAwpJREFUSA21Vt1PUmEYP4dvkQ8JFMwtBRocWAkDbiqXrUWXzU1rrTt0bdVqXbb1tbW16C9IBUSmm27cODdneoXjputa6069qwuW6IIBIdLvdaF4OAcOiGeDc87zPs/vd57P96WpFq7p6enbGo1mjKZpeTabjU1MTCRagGnOZHFxcXxtbe1XKpUq7+zslJeXl//Mz8+Hy+Uy3RxSE9qTk5M3otFooVQqgef4Wl9f343FYoEmoISrxuNxFX5f9vb2jhn/PxUKhfLS0tIPfFifUESRUMV8Pv/M6XReRm5rTGQyGeXxeGxYe1ezeBpBOBx2rKysbO7v79d4Wy3Y2Nj4GQqFbgnhaugxwiuGJx99Pp9FLBbXxYTXvTqd7v3MzIy6riIWGxJnMpl7AwMD14xGYyMsSq1WUyQdUqn0eSPlusQIsbGrq+vl4OCgvhFQZd1utyv1en0gEolcqsi47nWJlUrlG5fLZVcoFFy2nDKSDpIWlUoVTCQSEk4lCHmJMZ2GTCbTiMVikfIZ88l7enoos9l8dXt7+z6fDicxSJUokqDX6xXcl2wCROoc0vQCWL3sNfLOSdzR0fHY4XC4tVotl40gmVwup9xuN4OQv+UyqCFGH9rg7SOGYVRcBs3IEG4J0nVnamrqOtvuBDGGgQg9+wHFcVEi4a0LNkbdd6TrPKo8ODc311mteIIYjT/a398/jK+s1jnVM0kXoufCFvq0GuiIGEVgQIhfoygM1QrteEa9dAL7ITiYCt4RMabOK5AyKKzKWtvupLcRciu8D5J0EuDDPyT/Snd39yh6VtY2NhYQSR9G79Ds7OxdskRjEyAufvb7/cPoO5Z6e1+xtVKrq6vfcFzyi/A3ZrPZ3GdNSlwgo5ekE4X2RIQGf2C1WlufFE0GBeGWYQ8YERWLxQtnUVB830MKLZfL9RHir8lkssCn2G751tZWEWe03zTKm15YWPiEiXXTYDB0Ig/t7yd8PRws4EicwWHxO4jHD8/C5HiTTqd1BwcHFozKU89origB+y/kmzgYpgOBQP4fGmUiZmJ+WNgAAAAASUVORK5CYII=')
}
.arrow {
  float: right;
  width: 12px;
  height: 15px;
  background-repeat: no-repeat;
  background-size: contain;
  background-position-y: bottom;
}

.number {
  display: inline-block;
  padding: 4px 10px;
  color: #FFF;
  border-radius: 4px;
  background: #44475C;
  margin: 0px 5px;
  cursor: pointer;
}
.number:hover, .number.active {
  background: #717699;
}
#DetailsChart {
  width: 100%;
  height: 500px;
}
.modal {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 9;
  overflow-x: hidden;
  overflow-y: auto;
  &__backdrop {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 1;
  }
  &__dialog {
    position: relative;
    width: 1200px;
    // height: 1200px;
    background-color: #ffffff;
    border-radius: 5px;
    margin: 50px auto;
    display: flex;
    flex-direction: column;
    z-index: 2;
    @media screen and (max-width: 992px) {
      width: 90%;
    }
  }
  &__close {
    width: 30px;
    height: 30px;
  }
  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 20px 20px 10px;
  }
  &__body {
    padding: 10px 20px 10px;
    overflow: auto;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  &__footer {
    padding: 10px 20px 20px;
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.overflow-hidden {
  overflow: hidden;
}
</style>