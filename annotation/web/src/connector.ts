import { DEVMODE } from './globals'

let SERVER_LOG_ROOT = DEVMODE ? "http://127.0.0.1/" : "https://quest.ms.mff.cuni.cz/mmsg/"
export let IMGDATA_ROOT = "https://vilda.net/s/diffusion-annotations/img_data/"

export async function load_data(): Promise<any> {
    let result = await $.ajax(
        SERVER_LOG_ROOT + "get_log",
        {
            data: JSON.stringify({ uid: globalThis.uid }),
            type: 'POST',
            contentType: 'application/json',
        }
    )

    result = JSON.parse(result)
    if (result["new_user"] == "yes") {
        alert(
            "Your logfile was not found on the server and I'm serving you the default queue (all images). "
            + "This may be an error if you were in contact with Vilém about this experiment before. "
            + "Please make sure that your entered user id is correct and in case of repeated failure, contact Vilém."
        )
    }
    return result["data"]
}

// dumps all the data which is long-term unsustainable but since the image is not part of the payload
// it's expected to be <100k
export async function log_data(): Promise<any> {
    let result = await $.ajax(
        SERVER_LOG_ROOT + "log",
        {
            data: JSON.stringify({ data: globalThis.data, uid: globalThis.uid }),
            type: 'POST',
            contentType: 'application/json',
        }
    )
    return result
}