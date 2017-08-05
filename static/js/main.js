var map = new Datamap({scope: 'world', element: document.getElementById('map_container'), responsive: true,
    dataUrl: '/data',
    fills: {
       'No information': 'gray',
        defaultFill: 'gray'
    },
     geographyConfig: {
        borderColor: 'black',
        borderWidth: 0.5,
        popupTemplate: function(geo, data) {
            if (!data){
                return ['<div class="hoverinfo"><strong>',
                    geo.properties.name,
                    '<br> No data available </strong></div>'].join('');
            } else {
                var country_info_list = data.country_info[0];
                var info_string = "";
                for (var index in country_info_list){
                    info_string += country_info_list[index]['project_name'];
                    info_string += " : ";
                    info_string += country_info_list[index]['lendprojectcost'];
                    info_string += "<br>";
                }
                return ['<div class="hoverinfo"><strong>',
                    geo.properties.name,
                    '<br> ' + 'Total: '+ data.country_info[1],
                    '<br>' + 'Project Name : Project Cost ',
                    '<hr>', info_string,'</strong></div>'].join('');
            }
        }
    }
});

// 1st part of legend ( title and 'No information' rectangle )
var legend_options = {legendTitle:'Projects cost distribution by countries'};
map.legend(legend_options);

//2nd part of legend ( color mapping with cost min & max values)
var width = 400;
var height = 50;
var color = d3.interpolateOrRd;

data = [{"label":"250.000 >"},
        {"label":""},
        {"label":""},
        {"label":""},
        {"label":""},
        {"label":""},
        {"label":""},
        {"label":""},
        {"label":"< 6.443.900.000"}];

var legend = d3.select("#map_container").append("svg")
    .attr("class", "legend")
    .attr("width", width)
    .attr("height", height)
    .selectAll("g")
    .data(data)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate("+i*20+',0' + ")"; });

legend.append("rect")
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", function(d, i) {
                                // from 0.1 to 1 range
                                return color(i/10+0.1); });

legend.append("text")
    .attr("x", 0)
    .attr("y", 36)
    .attr("dy", ".35em")
    .text(function(d) {return d.label; });
