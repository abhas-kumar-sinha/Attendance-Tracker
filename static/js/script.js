toggle = document.querySelector(".toggle");
sidebar = document.querySelector(".side-bar");
logout = document.querySelector(".nav-link-1");
courseAnalytics = document.querySelector(".course-analytics")
listSbOptions = document.querySelectorAll(".nav-link a")

async function fetchAtData() {
    try {
        // Get the text content of the element with ID "attendance"
        attendanceDataEle = document.querySelector("#attendance").textContent;

        // Parse JSON data
        attendanceData = JSON.parse(attendanceDataEle);

        if (attendanceData.length != 0) {
            let num=0
            attendanceData.forEach(course => {
                num++
                newCourseDiv = document.createElement('div');
                newCourseDiv.classList.add(`course-${num}`, 'course');
                courseAnalytics.appendChild(newCourseDiv);

                if (course[1]['LECTURE']+course[1]['LAB']+course[1]['TUTORIAL']+course[1]['INTRODUCTION'] == 0 
                    && course[2]['LECTURE']+course[2]['LAB']+course[2]['TUTORIAL']+course[2]['INTRODUCTION'] == 0 
                    && course[3]['LECTURE']+course[3]['LAB']+course[3]['TUTORIAL']+course[3]['INTRODUCTION'] == 0){
                    newHead = document.createElement('h2');
                    newpara = document.createElement('p');
                    newHead.textContent = `${course[0]}`
                    newpara.textContent = "No Data to display."
                    newHead.classList.add('analytics-div-head');
                    newpara.classList.add('analytics-div-para');
                    newCourseDiv.appendChild(newHead);
                    newCourseDiv.appendChild(newpara);
                } else{
                    let pie = new ej.charts.AccumulationChart({
                        series: [
                            {
                    
                                dataSource: [
                                    { x: 'Present', y: course[1]['LECTURE']+course[1]['LAB']+course[1]['TUTORIAL']+course[1]['INTRODUCTION'], r: '92.5' },
                                    { x: 'Absent', y: course[2]['LECTURE']+course[2]['LAB']+course[2]['TUTORIAL']+course[2]['INTRODUCTION'], r: '92.5' },
                                    { x: 'Medical leave', y: course[3]['LECTURE']+course[3]['LAB']+course[3]['TUTORIAL']+course[3]['INTRODUCTION'], r: '92.5' },
                                ],
                                dataLabel: {
                                    visible: false, position: 'none',
                                    name: 'x'
                    
                                },
                                radius: 'r', xName: 'x',
                                yName: 'y', innerRadius: '20%'
                            },
                    
                        ],
                        enableSmartLabels: false,
                        legendSettings: {
                            visible: true,
                        },
                        enableAnimation: true,
                        title: `${course[0]} Attendance`
                    }, '#element');
                    
                    pie.appendTo(newCourseDiv);
                }
            });
        } else{
            alertDiv = document.createElement('div')
            alertDiv.classList.add('alert-div')
            alertDiv.innerHTML += `
            <h1>No Courses To Display. </h1>
            <a href="Add-Course" class="sub-alert-div">
                <i class='bx bx-book-add'></i>
                <p>Add course</p>
            </a>`
            courseAnalytics.appendChild(alertDiv);
        }

    } catch (error) {
        temp=1;
    }
};

currPage = window.location.pathname;

if (currPage == "/Home") {
    listSbOptions[0].classList.add("is-active")
    
    fetchAtData()
    }
if (currPage == "/Add-Course") {
    listSbOptions[1].classList.add("is-active")
}
if (currPage == "/Mark-Attendance") {
    listSbOptions[2].classList.add("is-active")
}
if (currPage == "/Analytics") {
    listSbOptions[4].classList.add("is-active")

    fetchAtData()
}
if (currPage == "/Today-Schedule") {
    listSbOptions[3].classList.add("is-active")
}
if (currPage == "/Grades") {
    listSbOptions[5].classList.add("is-active")
}

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close")
})

sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close") 
})

sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close") 
})