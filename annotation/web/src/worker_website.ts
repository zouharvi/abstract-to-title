import { IMGDATA_ROOT, log_data } from "./connector"

let title_area_table = $("#title_area_table_body")

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length},
        <strong>UID:</strong> ${globalThis.uid},
        <strong>type:</strong> ${globalThis.data_now["type"]}
    `)
    $("#abstract").text(globalThis.data_now["abstract"])
}

function load_cur_abstract() {
    load_headers()

    switch (globalThis.data_now["type"]) {
        case "all_direct": load_cur_abstract_all_direct(); break;
        case "all_direct_ref": load_cur_abstract_all_direct_ref(); break;
    }
}
    
function load_cur_abstract_all_direct() {
    title_area_table.html("")
    globalThis.data_now["titles_order"].forEach((title_order: string, title_i: number) => {
        let new_an = $(`
            <tr>
                <td>• ${globalThis.data_now["titles"][title_order]}</td>
                <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
            </tr>
        `)
        title_area_table.append(new_an);
        bind_labels(title_i);
    })


    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });

        // space for comments
        globalThis.data_now["response"].push("")
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}

function load_cur_abstract_all_direct_ref() {
    title_area_table.html("")
    globalThis.data_now["titles_order"].forEach((title_order: string, title_i: number) => {
        let new_an;
        if (title_i == 0) {
            new_an = $(`
            <tr>
                <td><b>Reference:</b> ${globalThis.data_now["titles"][title_order]}</td>
            </tr>
        `)
        } else {
            new_an = $(`
                <tr>
                    <td>• ${globalThis.data_now["titles"][title_order]}</td>
                    <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
                </tr>
            `)
        }
        title_area_table.append(new_an);
        bind_labels(title_i);
    })


    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });

        // space for comments
        globalThis.data_now["response"].push("")
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}

function bind_labels(title_i: number) {
    $("#q_" + title_i.toString()).on('input change', function () {
        let val = parseInt($(this).val() as string);
        globalThis.data_now["response"][title_i] = val;

        let slider_obj_val = $("#q_" + title_i.toString() + "_val");
        slider_obj_val.text(val)
    });

    // special handling of default "empty" value
    $("#q_" + title_i.toString()).on('click', function () {
        if (globalThis.data_now["response"][title_i] == -1) {
            globalThis.data_now["response"][title_i] = 0;

            let val = parseInt($(this).val() as string);
            console.log(val)
            let slider_obj_val = $("#q_" + title_i.toString() + "_val");
            slider_obj_val.text(val)
        }
    });
}

function setup() {
    // send current data
    // load next abstract
    $("#but_next").on("click", () => {
        globalThis.data_i += 1;
        if (globalThis.data_i >= globalThis.data.length) {
            alert("You completed the whole queue, thanks! Wait a few seconds to finish synchronization.");
            globalThis.data_i = 0;
        }
        
        globalThis.data_now = globalThis.data[globalThis.data_i];
        log_data()
        load_cur_abstract()
    })

    $("#but_prev").on("click", () => {
        globalThis.data_i -= 1;
        // modulo
        if (globalThis.data_i < 0) {
            globalThis.data_i = globalThis.data.length - 1;
        }
        
        globalThis.data_now = globalThis.data[globalThis.data_i];
        log_data()
        load_cur_abstract()
    })
}


export { setup, load_cur_abstract }