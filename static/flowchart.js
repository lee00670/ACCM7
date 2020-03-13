/*function myFunc() {
    return flowchart_list
}*/



const program_map = {
    'nodes':[
        // level 1
        {
            'id': flowchart_courses[0].id,
            'courseid': flowchart_courses[0].ccode,
            //'coursename': flowchart_courses[0].coursename,

            'xcoord': 90,
            'ycoord': 10,
            'port': ['left', 'bottom', 'right']
        },
        {
            'id': flowchart_courses[2].id,
            'courseid': flowchart_courses[2].ccode,
            //'coursename': flowchart_courses[2].coursename,

            'xcoord': 270,
            'ycoord': 10,
            'port': ['left', 'bottom']
        },
        {
            'id': flowchart_courses[4].id,
            'courseid': flowchart_courses[4].ccode,
            //'coursename': flowchart_courses[4].coursename,

            'xcoord': 450,
            'ycoord': 10,
            'port': ['bottom']
        },
        {
            'id': flowchart_courses[6].id,
            'courseid': flowchart_courses[6].ccode,
            //'coursename': flowchart_courses[6].coursename,

            'xcoord': 630,
            'ycoord': 10,
            'port': []
        },
        {
            'id': flowchart_courses[8].id,
            'courseid': flowchart_courses[8].ccode,
            //'coursename': flowchart_courses[8].coursename,

            'xcoord': 810,
            'ycoord': 10,
            'port': []
        },
        {
            'id': flowchart_courses[10].id,
            'courseid': flowchart_courses[10].ccode,
            //'coursename': flowchart_courses[10].coursename,

            'xcoord': 990,
            'ycoord': 10,
            'port': []
        },

        // level 2
        {
            'id': flowchart_courses[12].id,
            'courseid': flowchart_courses[12].ccode,
            //'coursename': flowchart_courses[12].coursename,

            'xcoord': 90,
            'ycoord': 220,
            'port': ['top']
        },
        {
            'id': flowchart_courses[14].id,
            'courseid': flowchart_courses[14].ccode,
            //'coursename': flowchart_courses[14].coursename,

            'xcoord': 270,
            'ycoord': 220,
            'port': ['top', 'bottom']
        },
        {
            'id': flowchart_courses[15].id,
            'courseid': flowchart_courses[15].ccode,
            //'coursename': flowchart_courses[15].coursename,

            'xcoord': 450,
            'ycoord': 220,
            'port': []
        },
        {
            'id': flowchart_courses[16].id,
            'courseid': flowchart_courses[16].ccode,
            //'coursename': flowchart_courses[16].coursename,

            'xcoord': 630,
            'ycoord': 220,
            'port': []
        },
        {
            'id': flowchart_courses[17].id,
            'courseid': flowchart_courses[17].ccode,
            //'coursename': flowchart_courses[17].coursename,

            'xcoord': 810,
            'ycoord': 220,
            'port': ['bottom']
        },
        {
            'id': 12,
            'courseid': 'GED3002',
            'coursename': 'General Education Elective',

            'xcoord': 990,
            'ycoord': 220,
            'port': []
        },

        // level 3
        {
            'id': flowchart_courses[18].id,
            'courseid': flowchart_courses[18].ccode,
            //'coursename': flowchart_courses[18].coursename,

            'xcoord': 90,
            'ycoord': 430,
            'port': ['left', 'top']
        },
        {
            'id': flowchart_courses[19].id,
            'courseid': flowchart_courses[19].ccode,
            //'coursename': flowchart_courses[19].coursename,

            'xcoord': 270,
            'ycoord': 430,
            'port': ['left', 'bottom']
        },
        {
            'id': flowchart_courses[20].id,
            'courseid': flowchart_courses[20].ccode,
            //'coursename': flowchart_courses[20].coursename,

            'xcoord': 450,
            'ycoord': 430,
            'port': ['top', 'right']
        },
        {
            'id': flowchart_courses[22].id,
            'courseid': flowchart_courses[22].ccode,
            //'coursename': flowchart_courses[22].coursename,

            'xcoord': 810,
            'ycoord': 430,
            'port': ['top']
        },
        {
            'id': 17,
            'courseid': 'GED3002',
            //'coursename': 'General Education Elective',

            'xcoord': 990,
            'ycoord': 430,
            'port': []
        },

        // level 4
        {
            'id': flowchart_courses[23].id,
            'courseid': flowchart_courses[23].ccode,
            //'coursename': flowchart_courses[23].coursename,

            'xcoord': 90,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[24].id,
            'courseid': flowchart_courses[24].ccode,
            //'coursename': flowchart_courses[24].coursename,

            'xcoord': 270,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[25].id,
            'courseid': flowchart_courses[25].ccode,
            //'coursename': flowchart_courses[25].coursename,

            'xcoord': 450,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[26].id,
            'courseid': flowchart_courses[26].ccode,
            //'coursename': flowchart_courses[26].coursename,

            'xcoord': 630,
            'ycoord': 640,
            'port': ['top']
        },
    ],
    // prerequisite links
    'links': [
        {
            'source': {
                'id': prerequisite_links[4].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[4].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[0].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[0].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[5].source_id,
                'port': 'right'
            },
            'target': {
                'id': prerequisite_links[5].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[6].source_id,
                'port': 'left'
            },
            'target': {
                'id': prerequisite_links[6].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[1].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[1].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[2].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[2].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[3].source_id,
                'port': 'left'
            },
            'target': {
                'id': prerequisite_links[3].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[7].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[7].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[8].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[8].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[9].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[9].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[10].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[10].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[11].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[11].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[12].source_id,
                'port': 'right'
            },
            'target': {
                'id': prerequisite_links[12].target_id,
                'port': 'top'
            }
        }
    ]
}

var electives = [];
console.log("student_results", student_results);
// set grades and course info such as prof
for (var i = 0; i < program_map.nodes.length; i++) {
    for (var g = 0; g < student_results.length; g++) {
        if(program_map.nodes[i].courseid == student_results[g].ccode) {
            program_map.nodes[i].grade = student_results[g].grade;
            program_map.nodes[i].mapid = student_results[g].mapid;
            program_map.nodes[i].title = student_results[g].coursename;
            program_map.nodes[i].studentname = student_results[g].student_name;
            program_map.nodes[i].studentnum = student_results[g].student_num;
            program_map.nodes[i].gid = student_results[g].gid;
            //console.log(program_map.nodes[i].grade);
        }
    }
}

for (var g = 0; g < student_results.length; g++) {
        if (student_results[g].id == null) {
            //console.log(student_results[g].ccode);

            if (student_results[g].ccode !='MAT8001') {
                electives.push(student_results[g]);
            }
        }
    }

var elective_options = [];
for (var i = 0; i < program_map.nodes.length; i++) {
    if (program_map.nodes[i].courseid === 'GED3002') {
        elective_options.push(program_map.nodes[i]);
    }
}

if (electives.length == 1 ) {
    console.log(electives[0]);
    elective_options[0].grade = electives[0].grade;
    elective_options[0].mapid = electives[0].mapid;
    elective_options[0].gid = electives[0].gid;
    elective_options[0].title = electives[0].coursename;
}
else if (electives.length == 2) {
    elective_options[0].grade = electives[0].grade;
    elective_options[0].mapid = electives[0].mapid;
    elective_options[0].gid = electives[0].gid;
    elective_options[0].title = electives[0].coursename;

    elective_options[1].grade = electives[0].grade;
    elective_options[1].mapid = electives[0].mapid;
    elective_options[1].gid = electives[0].gid;
    elective_options[1].title = electives[0].coursename;
}

// graph: contains a reference to all components of your diagram
// graph is a model holding all cells (elements/links) which are stored in property 'cells'
var graph = new joint.dia.Graph;

joint.setTheme('modern');

// paper: responsible for rendering the graph
var paper = new joint.dia.Paper({
            el: $('div#flowchart'),
            model: graph,
            width: $('div#flowchart').width(),
            height: $('div#flowchart').height(),
            gridSize: 10,
            drawGrid: true,
            /*background: {
                color: 'rgba(0, 255, 0, 0.3)'
            }*/
});



// custom shape
joint.shapes.basic.CourseBox = joint.shapes.basic.Generic.extend({

    markup: [{
        tagName: 'rect',
        selector: 'box',
    }, {
        tagName: 'text',
        selector: 'courseCode'
    }, {
        tagName: 'text',
        selector: 'grade'
    }, {
        tagName: 'image',
        selector: 'editIcon'
    }, {
        tagName: 'image',
        selector: 'infoIcon'
    }],

    defaults: joint.util.defaultsDeep({

        type: 'basic.CourseBox',
        size: { width: 120, height: 110 },
        attrs: {
            'box': {
                fill: '#28A745', stroke: '#28A745', width: 120, height: 110,
                rx: 10,
                ry: 10,
                filter: {
                    name: 'dropShadow',
                    args: {
                        dx: 5,
                        dy: 5,
                        blur: 3
                    }
                },
                cursor: 'default'
            },
            //'courseName': { 'cursor': 'default', 'font-size': 13.5, text: '', 'ref-x': .5, 'ref-y': 25, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#ffffff' },
            'courseCode': { 'cursor': 'default', 'font-size': 16, 'font-weight': 'bold', text: '', 'ref-x': .5, 'ref-y': 30, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#ffffff' },
            'grade': { 'cursor': 'default', 'font-size': 16, 'font-weight': 'bold', text: '', 'ref-x': .5, 'ref-y': 60, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#ffffff' },
            /*'editGrade': { 'font-size': 16, 'font-weight': 'bold', text: 'Edit', 'ref-x': .6, 'ref-y': 120, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#00ccff',
            event: 'element:edit', cursor: 'pointer'},*/
            'editIcon': { 'xlink:href': '', 'ref-x': .75, 'ref-y': 78, ref: 'box', width: 25, height: 28,  event: 'element:edit', cursor: 'pointer'},
            'infoIcon': { 'xlink:href': '', 'ref-x': 5, 'ref-y': 76, ref: 'box', width: 30, height: 30,  event: 'element:info', cursor: 'pointer'}
        },
        // define port groups
    ports: {
        groups: {
            'left': {
                position: {
                    name: 'left'
                },
                attrs: {
                    circle: { fill: '#3498DB', r: 0.5, magnet: true}
                }
            },
            'bottom': {
                position: {
                    name: 'bottom'
                },
                attrs: {
                    circle: { fill: '#3498DB', r: 0.5, magnet: true}
                }
            },
            'right': {
                position: {
                    name: 'right'
                },
                attrs: {
                    circle: { fill: '#3498DB', r: 0.5, magnet: true}
                }
            },
            'top': {
                position: {
                    name: 'top'
                },
                attrs: {
                    circle: { fill: '#3498DB', r:0.5, magnet: true}
                }
            }
        }

    }

    }, joint.shapes.basic.Generic.prototype.defaults)
});


var courseList = program_map.nodes;
var prereqlinks = program_map.links;
var i;
var createdCourses = [];
var portsides = ['top', 'right', 'bottom', 'left'];

// loop through course list to create shape for each
for (i=0; i < courseList.length; i++) {
    var course = new joint.shapes.basic.CourseBox({
    position: { x: courseList[i].xcoord, y: courseList[i].ycoord },
    size: { width: 120, height: 110 },
    id: courseList[i].id,
    attrs: {
        //courseName: { text: joint.util.breakText(courseList[i].coursename, { width: 150 })},
        courseCode: { text: courseList[i].courseid},
        infoIcon: { 'xlink:href':  '/static/info-icon.png'}
    }
});

    if (courseList[i].grade === "" || courseList[i].grade == undefined) {
        course .attr('grade/display', 'none');
    }
    else {
        course.attr('grade/text', 'Grade: '+ courseList[i].grade);
        course.attr('editIcon/xlink:href', '/static/edit-icon.png');
    }

    // add ports
    for (var s=0; s < portsides.length; s++) {
        for (var p=0; p < courseList[i].port.length; p++) {
            if (courseList[i].port[p] === portsides[s]) {
                course.addPort({group: portsides[s], magnet: true, attrs: {cursor: 'default'}});
            }
        }
    }


    createdCourses.push(course);
    course.addTo(graph);
}

// add links
for (var l=0; l < prereqlinks.length; l++) {
    var link = new joint.shapes.standard.Link({
        source: prereqlinks[l].source,
        target: prereqlinks[l].target,
        connector: {name: 'rounded'},
        router: {
            name: 'manhattan',
            args: {
                step: 15,
                startDirections: [prereqlinks[l].source.port],
                endDirections: [prereqlinks[l].target.port],
                maximumLoops: 300
            }
        },
        attrs: {
            line: {
                strokeWidth: 4,
                stroke: '#000000',
                cursor: 'default'
            }
        }
    });

    link.addTo(graph);
}


// prevent moving shapes
paper.setInteractivity({elementMove: false});

// paper event edit
paper.on('element:edit', function(elementView, evt, x, y) {
        var getGrade;
        var getCourseId;
        var getMapid;
        var getTitle;
        var getName;
        var getGid;
        var k;
        var j;
        for(k=0; k<courseList.length; k++){
            if(courseList[k].id === elementView.model.id) {
                getGrade = courseList[k].grade;
                getCourseId = courseList[k].courseid;
                getMapid = courseList[k].mapid;
                getTitle = courseList[k].title;
                getName = courseList[k].studentname;
                getNum = courseList[k].studentnum;
                getGid = courseList[k].gid;

            }
        }
        //alert('Edit grade: ' + getGrade + ' for course code '+ getCourse + ' ' + getMapid);
        //$('#modal-launch').attr('data-target','#modalLoginForm');


        // edit modal
        $('#editGradeFlowchart').modal('show');
        $('input#courseCode').val(getCourseId);
        $('input#gradeID').val(getGid)
        $('input#courseTitle').val(getTitle);
        $('input#inputGradeFlowchart').val(getGrade);
        $('input#mapid').val(getMapid);


    }
);



// paper event edit
paper.on('element:info', function(elementView, evt, x, y) {
        var getGrade;
        var getCourseId;
        var getMapid;
        var getTitle;
        var getName;
        var getGid;
        var k;
        for(k=0; k<courseList.length; k++){
            if(courseList[k].id === elementView.model.id) {
                getGrade = courseList[k].grade;
                getCourseId = courseList[k].courseid;
                getMapid = courseList[k].mapid;
                getTitle = courseList[k].title;
                getName = courseList[k].studentname;
                getNum = courseList[k].studentnum;
                getGid = courseList[k].gid;
            }
        }
        //alert('Edit grade: ' + getGrade + ' for course code '+ getCourse + ' ' + getMapid);
        //$('#modal-launch').attr('data-target','#modalLoginForm');



        // info modal
        $('#infoFlowchart').modal('show');
        $('input#infocourseCode').val(getCourseId);
        $('input#infocourseTitle').val(getTitle);
        $('input#mapid').val(getMapid);

    }
);



