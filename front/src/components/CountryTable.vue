<template>
  <div id="CountryTable">
    <div id="couOver">
      <!-- <button>Invalidate</button> -->
    </div>
    <div id="selectordiv">
    </div>
    <button v-on:click="refresh()">Invalidate</button>
   <table>
     <thead>
       <tr>
         <th v-for="(col, index) in columns" :key="col" >{{col}}
           <div class="arrow" v-if="col == sortColumn" v-bind:class="[ascending ? 'arrow_up' : 'arrow_down']"></div>
           <div v-if="index > 1 && index < 9">
            <input type="checkbox" :id="col" v-on:click="datashown(col)" :checked="datashowing[col]">
           </div>
            <button class="sort_button" v-on:click="sortTable(col)">Sort</button>
         </th>
         <th>
             Shown
         </th>
       </tr>
     </thead>
     <tbody>
       <tr v-for="(row, index) in get_rows()" :key="row">
         <td v-for="col in columns" :key="col">{{row[col]}}</td>
         <td :id="row.id"><input type="checkbox" :id="row.id" v-on:click="shown(row.id)" :checked="Shown[row.id]"></td>
       </tr>
     </tbody>
  </table>
  <div class="pagination">
    <div class="number"
         v-for="i in num_pages()"
         :key="i"
         v-bind:class="[i == currentPage ? 'active' : '']"
         v-on:click="change_page(i)">{{i}}</div>
  </div>
</div>
</template>

<script type="module">
    // import HelloWorld from './HelloWorld.vue'
    // import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'
    // import Vue from "vue"
    import Vue from "vue/dist/vue.esm.browser.min.js"
    // import Vue from 'https://unpkg.com/vue@2.6.0/dist/vue.esm.browser.min.js';
//   import HelloWorld from 'HelloWorld'
    import HelloWorld from './HelloWorld.vue'
    import * as am4plugins_rangeSelector from "@amcharts/amcharts4/plugins/rangeSelector"; 
    import * as am4charts from "@amcharts/amcharts4/charts";
    import * as am4core from "@amcharts/amcharts4/core";
    import am4themes_animated from "@amcharts/amcharts4/themes/animated";
    import axios from "axios";
import { cos } from '@amcharts/amcharts4/.internal/core/utils/Math';

    

    // console.log(HelloWorld.methods.test(1));
    







    export default{
        name: "CountryTable",
        data() {
            return {
                currentPage: 1,
                elementsPerPage: 12,
                ascending: false,
                sortColumn: '',
                rows: [
                    { id: 1, name: "Chandler Bing", phone: '305-917-1301', profession: 'IT Manager' },
                    { id: 2, name: "Ross Geller", phone: '210-684-8953', profession: 'Paleontologist' },
                    { id: 3, name: "Rachel Green", phone: '765-338-0312', profession: 'Waitress'},
                    { id: 4, name: "Monica Geller", phone: '714-541-3336', profession: 'Head Chef' },
                    { id: 5, name: "Joey Tribbiani", phone: '972-297-6037', profession: 'Actor' },
                    { id: 6, name: "Phoebe Buffay", phone: '760-318-8376', profession: 'Masseuse' }
                ],
                realrows: null,
                Shown: {},
                Data_Showing: {
                  "仍在治疗": false,
                  "新增死亡": false,
                  "新增确诊": false,
                  "累计死亡": false,
                  "累计治愈": false,
                  "累计确诊": true,
                  "重症病例": false,
                },
                showing: "累计确诊",
                chart: null,
                series: null,
                selector: null
                }
        },
        mounted() {
            // console.log(this.columns);
            // console.log(document.getElementById("countryTable"));
            HelloWorld.methods.get_data(1, function(result){
                // console.log(result);
                this.rows = [...result];
                this.realrows = [...this.rows];
                // this.Shown = [];
                result.forEach(function(cou, ind){
                    // console.log(cou.id);
                    this.Shown[cou.id] = true;
                    // console.log(cou.id);
                }.bind(this));
                // this.rowss = result;
                // console.log("Shown!");
                // console.log(this.Shown);
            }.bind(this));





            axios.get("http://127.0.0.1:5000/api/overview"+this.showing)
              .then( function(Response) {
                am4core.useTheme(am4themes_animated);

                var chart = am4core.create("couOver", am4charts.XYChart);
                this.chart = chart;
                // console.log(chart);

                // chart.language.locale = am4lang_es_ES;

                chart.paddingRight = 20;

                var data = [];
                var visits = 10;
                for (var i = 1; i < 50000; i++) {
                  visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
                  data.push({ date: new Date(2018, 0, i), value: visits });
                }

                var dates_t = [...Response.data.dates]
                dates_t.forEach(function(date, index){
                  Response.data.dates[index].date = new Date(date.date);
                });
                // console.log(data);
                chart.data = Response.data.dates;
                // console.log(Response.data.dates);

                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.grid.template.location = 0;
                dateAxis.minZoomCount = 5;


                // this makes the data to be grouped
                dateAxis.groupData = true;
                dateAxis.groupCount = 500;

                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

                var series = chart.series.push(new am4charts.LineSeries());
                this.series = series;
                series.dataFields.dateX = "date";
                series.dataFields.valueY = this.showing;
                series.tooltipText = "{valueY}";
                series.tooltip.pointerOrientation = "vertical";
                series.tooltip.background.fillOpacity = 0.5;

                chart.cursor = new am4charts.XYCursor();
                chart.cursor.xAxis = dateAxis;

                var scrollbarX = new am4core.Scrollbar();
                scrollbarX.marginBottom = 20;
                chart.scrollbarX = scrollbarX;

                // Add range selector
                var selector = new am4plugins_rangeSelector.DateAxisRangeSelector();
                this.selector = selector;
                selector.container = document.getElementById("selectordiv");
                selector.axis = dateAxis;

                chart.language.setTranslationAny("%1Y", "%1A");
                chart.language.setTranslationAny("%1M", "%1M");
                chart.language.setTranslationAny("YTD", "ESTE AÑO");
                chart.language.setTranslationAny("MAX", "TODO");
              }.bind(this));


              // var button = am4core.create("invalidate", am4core.PlayButton);
              //   button.events.on("toggled", function(event) {
              //     if (event.target.isActive) {
              //       console.log(event.target);
              //       console.log(event.target.setPropertyValue("isActive", false));
                    
              //     } else {
              //       console.log("526566");
              //     }
              //   });


            this.$root.$on('clear', function() {
              this.clear();
            }.bind(this));

            this.$root.$on('filter', function(Shown) {
              console.log("Filter!");
              this.filter(Shown);
            }.bind(this));




        },
        methods: {
            "update_overview": function update_overview() {
              axios.get("http://127.0.0.1:5000/api/overview"+this.showing)
              .then( function(Response) {
                this.chart.data = Response.data.dates;
                this.series.dataFields.valueY = this.showing;
              }.bind(this));
            },
            "sortTable": function sortTable(col) {
                if (this.sortColumn === col) {
                this.ascending = !this.ascending;
                } else {
                this.ascending = true;
                this.sortColumn = col;
                }

                var ascending = this.ascending;

                this.rows.sort(function(a, b) {
                if (a[col] > b[col]) {
                    return ascending ? 1 : -1
                } else if (a[col] < b[col]) {
                    return ascending ? -1 : 1
                }
                return 0;
                })
            },
            "num_pages": function num_pages() {
                return Math.ceil(this.rows.length / this.elementsPerPage);
            },
            "get_rows": function get_rows() {
                var start = (this.currentPage-1) * this.elementsPerPage;
                var end = start + this.elementsPerPage;
                return this.rows.slice(start, end);
            },
            "change_page": function change_page(page) {
                this.currentPage = page;
            },
            "shown": function shown(country_id) {
                this.Shown[country_id] = !this.Shown[country_id];
                console.log(this.Shown[country_id]);
                // console.log(HelloWorld.computed.get_general());
                this.$root.$emit('shown', this.Shown);
            },
            "datashown": function datashown(data_to_show) {
              this.Data_Showing[data_to_show] = !this.Data_Showing[data_to_show];
              this.showing = data_to_show;
              // this.Data_Showing["累计确诊"] = false;
              Object.keys(this.Data_Showing).forEach(function(key, index){
                if(key != data_to_show){
                  this.Data_Showing[key] = false;
                }
              }.bind(this));
              this.$root.$emit('datashowing', data_to_show);
              this.update_overview();
            },
            "refresh": function refresh() {
              var from = document.getElementsByClassName("amcharts-range-selector-from-input")[0].value;
              var to = document.getElementsByClassName("amcharts-range-selector-to-input")[0].value;
              console.log(from+to);
              axios.get("http://127.0.0.1:5000/api/countries_?from="+from+"&to="+to)
                .then( function(Response) {
                  this.rows = Response.data.countries;
                  this.realrows = [...this.rows]
                  // var temp = [this.rows]
                  // console.log(Response.data.countries);
                  this.$root.$emit('date_updated', [...this.rows]);
                }.bind(this));
              // console.log("Refresh!");
            },
            "filter": function filter(Shown) {
              var temp = [...this.realrows];
              this.realrows.forEach(function(cou, ind){
                // console.log(this.realrows);
                if(!Shown[cou.id]){
                  // console.log(cou.id);
                  if(temp.indexOf(cou)  > -1)
                    temp.splice(temp.indexOf(cou), 1);
                }
                // if(this.records[cou.id])
                //   this.records[cou.id].isActive = this.Shown[cou.id];
              }.bind(this));
              console.log("sadasdasd");
              this.rows = temp;
            },
            "clear": function clear() {
              this.rows = [...this.realrows];
            }
        },
        watch: {
            // "shown": function(data){
            //     console.log(data);
            // }
        },
        computed: {
            "columns": function columns() {
                // console.log(Object.keys(this.rows[0]));
                if (this.rows.length == 0) {
                    return [];
                }
                console.log(Object.keys(this.rows[0]));
                return Object.keys(this.rows[0]);
            },
            "datashowing": function datashowing() {
              return this.Data_Showing;
            }
        }
    };

    // export default CountryTable;

    // console.log("asdsasd");
    // console.log(HelloWorld);
    // console.log(countryTable);
</script>



<style scoped>
.hello {
  width: 100%;
  height: 500px;
}
table {
  font-family: 'Open Sans', sans-serif;
  width: 90%;
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
.sort_button {
  text-transform: uppercase;
  text-align: left;
  background: #c8a8db;
  color: #44475C;
  /* cursor: pointer; */
  padding: 1px;
  min-width: 10px;
}
#couOver {
  width: 100%;
  height: 500px;
  max-width: 100%;
}

#selectordiv {
  width: 100%;
  height: 30px;
}

</style>