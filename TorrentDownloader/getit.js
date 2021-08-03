const webtorrent = require('webtorrent-hybrid');
const fs = require('fs')
const path = require('path');
const parser = require('./parseURI')
const client = new webtorrent();

const bytesToSize = bytes => {
    if (bytes < 1024) {
        return `${bytes} b`
    } else {
        if (bytes < 1048576) {
            return `${(bytes / 1024).toFixed(2)} kb`
        }
        else {
            return `${(bytes / (1024 * 1024)).toFixed(2)} mb`
        }
    }
}

const torrent = process.argv[2]
// console.log(torrent)


if (torrent.length == 0 || torrent == undefined) {
    console.log(`torrent cannot be empty give URI in arguments`)
    process.exit(1)
}
else {
    var a = parser(torrent)
        .then(res => {
            if (res['type']) {

                process.stdout.write('\tstart downloading wait for some seconds\r')
                client.add(torrent, torrent => {
                    console.log(`File is start downloading at ${__dirname} with name "${torrent.name}" `)
                    const files = torrent.files;
                    var dirpath = "";

                    let length = files.length;
                    console.log("\t\tTotal files -> ", length)

                    if (length > 1) {
                        // make a folder and save files there
                        dirpath = torrent.name
                        fs.mkdir(dirpath, res => {
                            if (!res)
                                console.log(`All the files will save in the ${dirpath}`)
                        })
                    }

                    // Deselect all files on initial download to save downloading speed, make it one by one 
                    torrent.files.forEach((file, index) => {
                        file.deselect()
                        console.log(index + 1, file.name)
                    });
                    torrent.deselect(0, torrent.pieces.length - 1, false);

                    // const forLoop = async _ => {
                    //     console.log('Start')

                    //     for (let index = 0; index < length; index++) {
                    //         let name = path.join(dirpath,files[index].name)
                    //         process.stdout.write(`Downloading ${files[index].name}`);
                    //         files[index].select()
                    //         const stream = files[index].createReadStream();
                    //         const saveTo = fs.createWriteStream(name);
                    //         stream.on('end',_=>{
                    //             console.log(`file ${name} downloaded`);
                    //         }).pipe(saveTo) 
                    //     }

                    //     console.log('End')
                    // }
                    // forLoop()

                    files.forEach(async f => {
                        let name = path.join(dirpath, f.name)
                        process.stdout.write(`Downloading ${f.name}\n`);
                        f.select()
                        const stream = f.createReadStream();
                        const saveTo = fs.createWriteStream(name);
                        stream.on('end', _ => {
                            console.log(`file ${name} downloaded\n`);
                        }).pipe(saveTo)
                    })

                    torrent.on('download', function (bytes) {
                        process.stdout.write(`Total data downloaded : ${bytesToSize(torrent.downloaded)} && Progress : ${(torrent.progress * 100).toFixed(4)} % at ${bytesToSize(torrent.downloadSpeed)}/s                       \r`)
                    })

                    torrent.on('done', _ => {
                        console.log('torrent finished downloading')
                        client.destroy()
                    })
                    torrent.on('error', _ => {
                        console.log('ERROR in downloading torrent')
                        client.destroy()
                    })
                })

            }
            else {
                console.log("Torrent cannot parsed wrong link or hash check again")
                console.log(torrent)
                process.exit(1)
            }
        })
}