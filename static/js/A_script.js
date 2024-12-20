toggle = document.querySelector(".toggle");
sidebar = document.querySelector(".side-bar");
logout = document.querySelector(".nav-link-1");
courseAnalytics = document.querySelector(".course-analytics")
listSbOptions = document.querySelectorAll(".nav-link a")

async function fetchAtData() {
    try {
        attendanceDataEle = document.querySelector("#attendance").textContent;

        attendanceData = JSON.parse(attendanceDataEle);

        if (attendanceData.length != 0) {
            let num=0
            attendanceData.forEach(course => {
                num++
                wrapperDiv = document.createElement('div');
                wrapperDiv.classList.add('wrapper-div');
                wrapperDiv.setAttribute('id', `course-${num}`)
                newCourseDiv = document.createElement('div');
                newCourseDiv.classList.add(`course-${num}`, 'course');
                wrapperDiv.appendChild(newCourseDiv)
                calcDiv = document.createElement('div')
                calcDiv.classList.add('calc-div')
                calcDiv.innerHTML += `
                <h2>Attenance</h2>
                <div class="attendance-button-wrapper">
                <div class='show-attendance'>
                    <div class='present display-attendance'>
                        <p>Present</p>
                        <h1>${course[1]['LECTURE']+course[1]['LAB']+course[1]['TUTORIAL']+course[1]['INTRODUCTION']}</h1>
                    </div>
                    <div class='absent display-attendance'>
                        <p>Absent</p>
                        <h1>${course[2]['LECTURE']+course[2]['LAB']+course[2]['TUTORIAL']+course[2]['INTRODUCTION']}</h1>
                    </div>
                    <div class='mleave display-attendance'>
                        <p>Medical leave</p>
                        <h1>${course[3]['LECTURE']+course[3]['LAB']+course[3]['TUTORIAL']+course[3]['INTRODUCTION']}</h1>
                    </div>
                </div>
                <div class='calc-buttons'>
                    <button class='${course[0].replaceAll(" ", "_")} btns presence-btn'>Presence %</button>
                    <button class='btns leave-btn'>Leave calculator</button>
                </div>
                <div>
                `
                wrapperDiv.appendChild(calcDiv);
                courseAnalytics.appendChild(wrapperDiv);

                if (course[1]['LECTURE']+course[1]['LAB']+course[1]['TUTORIAL']+course[1]['INTRODUCTION'] == 0 
                    && course[2]['LECTURE']+course[2]['LAB']+course[2]['TUTORIAL']+course[2]['INTRODUCTION'] == 0 
                    && course[3]['LECTURE']+course[3]['LAB']+course[3]['TUTORIAL']+course[3]['INTRODUCTION'] ==0){
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
                                    { x: 'Present', y: course[1]['LECTURE']+course[1]['LAB']+course[1]['TUTORIAL']+course[1]['INTRODUCTION'], r: '100%' },
                                    { x: 'Absent', y: course[2]['LECTURE']+course[2]['LAB']+course[2]['TUTORIAL']+course[2]['INTRODUCTION'], r: '100%' },
                                    { x: 'Medical leave', y: course[3]['LECTURE']+course[3]['LAB']+course[3]['TUTORIAL']+course[3]['INTRODUCTION'], r: '100%' },
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
listSbOptions[4].classList.add("is-active")
fetchAtData()


toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close")
})

presenceCalc = document.querySelectorAll(".presence-btn");

presenceCalc.forEach(btn => {
    btn.addEventListener('click', () => {
        reqList=Array.from(btn.classList)
        course = reqList[0].replaceAll("_", " ")
        for (i = 0; i < attendanceData.length; i++) {
            if (attendanceData[i][0] == course) {
                sum_lecture = attendanceData[i][1]['LECTURE']+attendanceData[i][2]['LECTURE']+attendanceData[i][3]['LECTURE']
                if (sum_lecture != 0) {
                    ans_lecture = (attendanceData[i][1]['LECTURE']*100)/sum_lecture
                }else{
                    ans_lecture = 0
                }

                sum_tutorial = attendanceData[i][1]['TUTORIAL']+attendanceData[i][2]['TUTORIAL']+attendanceData[i][3]['TUTORIAL']
                if (sum_tutorial != 0) {
                    ans_tutorial = (attendanceData[i][1]['TUTORIAL']*100)/sum_tutorial
                }else{
                    ans_tutorial = 0
                }

                sum_lab = attendanceData[i][1]['LAB']+attendanceData[i][2]['LAB']+attendanceData[i][3]['LAB']
                if (sum_lab != 0) {
                    ans_lab = (attendanceData[i][1]['LAB']*100)/sum_lab
                }else{
                    ans_lab = 0
                }

                sum_introduction = attendanceData[i][1]['INTRODUCTION']+attendanceData[i][2]['INTRODUCTION']+attendanceData[i][3]['INTRODUCTION']
                if (sum_introduction != 0) {
                    ans_introduction = (attendanceData[i][1]['INTRODUCTION']*100)/sum_introduction
                }else{
                    ans_introduction = 0
                }

                break
            }
        }
        function ensureStringLengthFour(value) {
            let str = String(value);
        
            while (str.length < 4) {
                str = ' ' + str;
            }

            if (str.length > 4) {
                str = str.substring(0, 3);
            }
        
            return str;
        }

        ans_lecture = ensureStringLengthFour(ans_lecture);
        ans_tutorial = ensureStringLengthFour(ans_tutorial);
        ans_lab = ensureStringLengthFour(ans_lab);
        ans_introduction = ensureStringLengthFour(ans_introduction);

        alert(`Attendance in ${course} is      Percentage     |    Fraction
               In LECTURE                     : ${ans_lecture}      |     ${attendanceData[i][1]['LECTURE']}/${sum_lecture}
               In TUTORIAL                   : ${ans_tutorial}      |     ${attendanceData[i][1]['TUTORIAL']}/${sum_tutorial}
               In LAB                             : ${ans_lab}      |     ${attendanceData[i][1]['LAB']}/${sum_lab}
               In INTRODUCTION         : ${ans_introduction}      |     ${attendanceData[i][1]['INTRODUCTION']}/${sum_introduction}`)
    })
});

sideBarUpDiv = document.querySelector(".img-text")
navBar = document.querySelector(".nav-up")
photoDiv = document.querySelector(".profile-pic")

function isMobileDevice() {
    return /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

if (isMobileDevice()) {
    allNavOptions = document.querySelectorAll(".nav-up-bx")
    allNavOptions.forEach(option => {
        option.style.visibility = "hidden";
    });
    photoDiv.removeAttribute("href");
    toggle.style.display = "none";
    newMenu = document.createElement('div')
    newMenu.classList.add('new-menu')
    newMenu.innerHTML = `<i class='bx bx-menu'></i>`
    navBar.prepend(newMenu)

    newClose = document.createElement('div')
    newClose.classList.add('new-close')
    newClose.innerHTML = `<i class='bx bx-x'></i>`
    sideBarUpDiv.append(newClose)

    newDropDown =document.createElement('div')
    newDropDown.classList.add('new-drop-down')
    newDropDown.classList.add('new-drop-down-close')
    newDropDown.innerHTML = `<ul>
                                <li><a href="User-Profile">Profile</a></li>
                                <li><a href="Settings">Settings</a></li>
                                <li><a href="Settings">Message</a></li>
                                <li><a href="Settings">Notification</a></li>
                            </ul>`
    navBar.append(newDropDown)

    newMenu.addEventListener("click", () => {
        sidebar.classList.toggle("close")
        logout.classList.toggle("close")
        toggle.classList.toggle("close")
    })
    
    newClose.addEventListener("click", () => {
        sidebar.classList.toggle("close")
        logout.classList.toggle("close")
        toggle.classList.toggle("close")
    })

    photoDiv.addEventListener('click', () => {
        newDropDown.classList.toggle('new-drop-down-close')
    })

    document.addEventListener('click', (event) => {
        if (photoDiv.contains(event.target)) {
    
            newDropDown.classList.toggle('new-drop-down-close')
    
        } else if (newDropDown.contains(event.target)) {
    
            console.log("newDropDown clicked");
    
        } else {
            listOfAllClasses = newDropDown.classList
            if ("new-drop-down-close" in listOfAllClasses){
                console.log("Do nothing")
            } else{
                newDropDown.classList.add('new-drop-down-close')
            }
        }
    })

} else{
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
}