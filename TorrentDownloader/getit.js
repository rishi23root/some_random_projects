const webtorrent = require('webtorrent-hybrid');
const fs = require('fs')
const path = require('path');
const parser = require('./parseURI')
const client = new webtorrent();


// user input
const torrent = process.argv[2]
const pathToSave = process.argv[3] || __dirname
console.log(pathToSave)


const bytesToSize = bytes => {
    // convert into more readable form 

    if (bytes < 1024) {
        return `${bytes} b`
    } else {

        if (bytes < 1048576) {
            return `${(bytes / 1024).toFixed(2)} kb`
        }
        else {
            return `${(bytes / (1048576)).toFixed(2)} mb`
        }
    }
}


if (torrent == undefined || torrent.length == 0) {

    console.log(`torrent cannot be empty give URI in arguments`)
    process.exit(1)

}
else {

    parser(torrent)
        .then(res => {

            if (res['type']) {

                process.stdout.write('\tstart downloading wait for some seconds\r')

                client.add(torrent,
                    {
                        path: __dirname
                    }
                    , torrent => {

                        console.log(`File is start downloading at \x1b[36m${__dirname}\x1b[0m with name "${torrent.name}" `)
                        const files = torrent.files;
                        var dirpath = pathToSave;

                        let length = files.length;
                        console.log("\t\tTotal Files -> ", length)

                        if (length > 1) {

                            // make a folder and save files there
                            fs.mkdir(path.join(dirpath, torrent.name), res => {
                                if (!res)
                                    console.log(`All the files will save in the ${dirpath}`)
                            })
                        }


                        // Deselect all files on initial download to save downloading speed, make it one by one 
                        torrent.files.map(file => file.deselect());
                        torrent.deselect(0, torrent.pieces.length - 1, false);


                        // start downloading one file at a time 
                        console.log("Downloading....");
                        files.forEach(async (f,index) => {
                            let name = path.join(dirpath, f.path)
                            console.log(name)
                            console.log(index + 1, `${f.name} - ${bytesToSize(f.length)}\t\t`);
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
                            process.exit(1)

                        })
                        torrent.on('error', _ => {
                            console.log('ERROR in downloading torrent')
                            client.destroy()
                            process.exit(1)

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
