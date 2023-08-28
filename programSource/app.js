const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use('/videos', express.static(path.join(__dirname, 'videos')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// for index.html
app.get('/videos', (req, res) => {
    const videoDirectory = path.join(__dirname, 'videos'); // 동영상 파일이 있는 디렉토리 경로
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('디렉토리 읽기 오류:', err);
            return res.status(500).send('내부 서버 오류');
        }

        const videoList = files.filter(file => file.endsWith('.mp4'));
        const videoRows = videoList.map(video => {
            const videoName = video.replace('.mp4', ''); // '.mp4' 확장자 제거
            const nameParts = videoName.split('_'); // 밑줄('_')로 비디오 이름 나누기

            const originalName = nameParts[0];
            const part1 = nameParts[1];
            const part2 = nameParts[2];
            // 원하는 부분들을 각각 저장한 변수를 추가

            return `
                <tr>
                    <td>${originalName}</td>
                    <td>${part1}</td>
                    <td>${part2}</td>
                    <td>
                        <video width="320" height="240" controls>
                            <source src="/videos/${video}" type="video/mp4">
                        </video>
                    </td>
                    <td>${video}</td>
                </tr>`;
        }).join('');

        const index = `
            <table>
                <thead>
                </thead>
                <tbody>
                    ${videoRows}
                </tbody>
            </table>
        `;

        res.send(index);
    });
});

// for user.html
app.get('/original-names', (req, res) => {
    const videoDirectory = path.join(__dirname, 'videos');
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('디렉토리 읽기 오류:', err);
            return res.status(500).json([]);
        }

        const videoList = files.filter(file => file.endsWith('.mp4'));
        const originalNames = [...new Set(videoList.map(video => video.split('_')[0]))];

        res.json(originalNames);
    });
});

app.get('/videos/:originalName', (req, res) => {
    const selectedOriginalName = req.params.originalName;
    const videoDirectory = path.join(__dirname, 'videos');
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('디렉토리 읽기 오류:', err);
            return res.status(500).send('내부 서버 오류');
        }

        const videoList = files.filter(file => file.endsWith('.mp4'));
        const filteredVideos = videoList.filter(video => video.startsWith(selectedOriginalName));

        const videoRows = filteredVideos.map(video => {
            const videoName = video.replace('.mp4', '');
            const nameParts = videoName.split('_');

            const originalName = nameParts[0];
            const part1 = nameParts[1];
            const part2 = nameParts[2];

            return `
                <tr>
                    <td>${part1}</td>
                    <td>${part2}</td>
                    <td>
                        <video width="320" height="240" controls>
                            <source src="/videos/${video}" type="video/mp4">
                        </video>
                    </td>
                    <td>${video}</td>
                </tr>`;
        }).join('');

        const user = `
            <table>
                <thead>
                </thead>
                <tbody>
                    ${videoRows}
                </tbody>
            </table>
        `;

        res.send(user);
    });
});

// for event.html
app.get('/part1-list', (req, res) => {
    const videoDirectory = path.join(__dirname, 'videos');
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('디렉토리 읽기 오류:', err);
            return res.status(500).json([]);
        }

        const videoList = files.filter(file => file.endsWith('.mp4'));
        const part1List = [...new Set(videoList.map(video => video.split('_')[1]))];

        res.json(part1List);
    });
});

app.get('/videos/part1/:selectedPart1', (req, res) => {
    const selectedPart1 = req.params.selectedPart1;
    const videoDirectory = path.join(__dirname, 'videos');
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('디렉토리 읽기 오류:', err);
            return res.status(500).send('내부 서버 오류');
        }

        const videoList = files.filter(file => file.endsWith('.mp4'));
        const filteredVideos = videoList.filter(video => video.split('_')[1] === selectedPart1);

        const videoRows = filteredVideos.map(video => {
            const videoName = video.replace('.mp4', '');
            const nameParts = videoName.split('_');

            const originalName = nameParts[0];
            const part1 = nameParts[1];
            const part2 = nameParts[2];

            return `
                <tr>
                    <td>${originalName}</td>
                    <td>${part2}</td>
                    <td>
                        <video width="320" height="240" controls>
                            <source src="/videos/${video}" type="video/mp4">
                        </video>
                    </td>
                    <td>${video}</td>
                </tr>`;
        }).join('');

        const event = `
            <table>
                <thead>
                </thead>
                <tbody>
                    ${videoRows}
                </tbody>
            </table>
        `;

        res.send(event);
    });
});

app.listen(port, () => {
    console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
});
