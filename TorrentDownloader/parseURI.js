// this module will help in identify the correct url and return the hash value of the url which will be easy to pass in urls and read
const parseTorrent = require('parse-torrent')

var testA = 'magnet:?xt=urn:btih:7A4214FE458B4B70BF18905E2CF3AE9BE11D8B2C&dn=Buenavista.Social.Club.1999.Movie.Poster.jpg&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2F47.ip-51-68-199.eu%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce'
var testB = '7a4214fe458b4b70bf18905e2cf3ae9be11d8b2c';

// 1. check for corrent format and 
// 1.0 can be magnet:? 
// 1.1 40 length hash
// 2. then conver the data in different formates and return the dict 
// or it can give just error in parsing

function checkValid(torrent) {
    // return type=[URI, infoHash , null]
    var returntype = { 'type': null }
    return new Promise(resolve => {
        // check if link is valid and return the type
        if (torrent.match(/magnet:\?.*/) && torrent.length > 40) {
            // if it starts from the magnet and length is greater then 40  //console.log(12346)
            returntype['type'] = 'URI'
            resolve(returntype)
        } else if (torrent.length == 40) {
            // it may be a hash console.log(000)
            returntype['type'] = 'infoHash'
            resolve(returntype)
        } else {
            // it nither a hash or uri // console.log(-1)
            resolve(returntype)
        }
    })
}

// example :
// checkValid(testA)
//     .then(res=>console.log(res))

async function getInfo(torrent) {
    let type = await checkValid(torrent);
    try {
        var data = parseTorrent(torrent)
    } catch {
        var data = { 'error': 'Error in resolving the torrent' }
    }
    return { ...type, ...data }
}

// example :
// getInfo(testB).then(r=>console.log(r))

module.exports = getInfo;