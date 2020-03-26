let designFlag = true;
let imgFlag = false;
console.log(designFlag);
if (designFlag) {
    const docUnit01 = document.getElementById('top_page_nav');
    const targetImg = document.getElementById('top_making_site');
    /* デザイン変更box挿入 */
    let topPage = document.getElementById('top-page');
    let nElement = document.createElement('div');
    nElement.id = 'test_button';
    let boxStr = '<div><a href="#page_t" id="design_off">off</a> <a href="#page_t" id="color_bk">＜＜</a>メインカラー' +
        '<a href="#page_t" id="color_fw">＞＞</a><span id="color_code"></span></div>' +
        '<div><a href="#page_t" id="dStyleBack">＜＜</a>デザインスタイル<a href="#page_t" id="dStyleForward">＞＞</a>' +
        '<span id="codeDS"></span></div>';
    if (docUnit01 != null) {
        boxStr += '<div><a href="#page_t" id="buttonUnit01B">＜＜</a>topPageNav' +
            '<a href="#page_t" id="buttonUnit01F">＞＞</a><span id="codeUnit01"></span></div>';
    }
    if (targetImg != null) {
        boxStr += '<div><a href="#page_t" id="test_b2">＜＜</a>画像' +
            '<a href="#page_t" id="test_b1">＞＞</a><span id="img_name"></span></div>'
    }
    nElement.innerHTML = boxStr;
    document.body.insertBefore(nElement, topPage);
    let oElement = document.createElement('div');
    oElement.id = 'turn_on';
    oElement.innerHTML = '' + '<a href="#page_t" id="t_on">D_TEST</a>';
    document.body.insertBefore(oElement, topPage);
    const designOff = document.getElementById('design_off');
    const testBox = document.getElementById('test_button');
    const onBox = document.getElementById('turn_on');
    const designOn = document.getElementById('t_on');
    designOff.onclick = function () {
        testBox.style.display = 'none';
        onBox.style.display = 'block'
    };
    designOn.onclick = function () {
        testBox.style.display = 'block';
        onBox.style.display = 'none'
    };
    /* 全体のデザイン方針 */
    const dsNameAndNum = ['flat20', 'flat', 'material', 'retroModern'];
    const designStyleList = [['fs1'], ['fs2'], ['fs3'], ['']];
    let designStyleNum = 0;
    const dsForward = document.getElementById('dStyleForward');
    const dsBack = document.getElementById('dStyleBack');
    const dsCode = document.getElementById('codeDS');

    function changeDS(dsNum) {
        designStyleNum += dsNum;
        if (designStyleNum >= dsNameAndNum.length) {
            designStyleNum = 0
        } else if (designStyleNum < 0) {
            designStyleNum = dsNameAndNum.length - 1
        }

        for (let i = 0; i <= 2; i++) {
            let underBarDS = '_';
            if (designStyleList[designStyleNum][i] === '') {
                underBarDS = ''
            }
        }

        dsCode.innerText = dsNameAndNum[designStyleNum]
    }

    function changeDSF() {
        changeDS(1)
    }

    function changeDSB() {
        changeDS(-1)
    }

    dsForward.onclick = changeDSF;
    dsBack.onclick = changeDSB;
    /* 以下、パーツごとのjs */
    if (docUnit01 != null) {
        const listUnit01 = ['fs1', 'fs2', 'fs3', ''];
        const unit01Forward = document.getElementById('buttonUnit01F');
        const unit01Back = document.getElementById('buttonUnit01B');
        const codeUnit01 = document.getElementById('codeUnit01');
        let numUnit01 = [0];


        function changeCss(numU, numUnit, listUnit, docUnit, codeUnit, unitId) {
            numUnit[0] += numU;
            if (numUnit[0] >= listUnit.length) {
                numUnit[0] = 0
            } else if (numUnit[0] < 0) {
                numUnit[0] = listUnit.length - 1
            }
            let underBar = '_';
            if (listUnit[numUnit[0]] === '') {
                underBar = ''
            }
            docUnit.id = unitId + underBar + listUnit[numUnit[0]];
            codeUnit.innerText = unitId + underBar + listUnit[numUnit[0]]
        }

        function changeCss01F() {
            changeCss(1, numUnit01, listUnit01, docUnit01, codeUnit01, 'top_page_nav')
        }

        function changeCss01B() {
            changeCss(-1, numUnit01, listUnit01, docUnit01, codeUnit01, 'top_page_nav')
        }

        unit01Forward.onclick = changeCss01F;
        unit01Back.onclick = changeCss01B
    }

    /* image切り替えテスト用 */
    if (imgFlag) {
        const testImg = ['AdobeStock_300836921_Preview.jpeg', 'AdobeStock_307608347_Preview.jpeg',
            'AdobeStock_237910217_Preview.jpeg', 'AdobeStock_300836989_Preview.jpeg', 'AdobeStock_228440224_Preview.jpeg'];
        const testButton = document.getElementById('test_b1');
        const backButton = document.getElementById('test_b2');
        const imageName = document.getElementById('img_name');
        let testNum = 0;
        if (targetImg != null) {
            targetImg.style.backgroundImage = 'url("../images/photo_test/about_us/' + testImg[testNum] + '")'
        }

        function changeImg(chNum) {
            testNum += chNum;
            if (testNum >= testImg.length) {
                testNum = 0
            } else if (testNum < 0) {
                testNum = testImg.length - 1
            }
            console.log(testNum);
            targetImg.style.backgroundImage = 'url("../images/photo_test/about_us/' + testImg[testNum] + '")';
            imageName.innerText = testImg[testNum]
        }

        function nextImg() {
            changeImg(1)
        }

        function backImg() {
            changeImg(-1)
        }

        testButton.onclick = nextImg;
        backButton.onclick = backImg
    }
    /* 色切り替え */
    const testColor = ['#ffffff', 'darkcyan', '#000000', 'red'];
    const nextColor = document.getElementById('color_fw');
    const backColor = document.getElementById('color_bk');
    const colorCode = document.getElementById('color_code');
    let cNum = 0;

    function changeColor(chNum2) {
        cNum += chNum2;
        if (cNum >= testColor.length) {
            cNum = 0
        } else if (cNum < 0) {
            cNum = testColor.length - 1
        }
        console.log(testColor[cNum]);
        colorCode.innerText = testColor[cNum];

        /* 切り替えるクラスとstyleの色の位置を書き換えて追加する */
        const mainClBg = document.getElementsByClassName('main_cl_bg');
        for (let i = 0; i < mainClBg.length; i++) {
            mainClBg[i].style.backgroundColor = testColor[cNum];
        }
        /* ここまでを以下に追加 */
        const mainClBdb = document.getElementsByClassName('main_cl_bdb');
        for (let j = 0; j < mainClBg.length; j++) {
            mainClBdb[j].style.borderBottomColor = testColor[cNum];
        }

    }

    function nextC() {
        changeColor(1)
    }

    function backC() {
        changeColor(-1)
    }

    nextColor.onclick = nextC;
    backColor.onclick = backC
}