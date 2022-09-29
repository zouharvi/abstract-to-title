import { IMGDATA_ROOT, log_data } from "./connector"

let an_area_var = $("#an_area_var")

function num_to_answer(num: number) {
    switch (num) {
        case -1:
            return "?"
        case 0:
            return "Definitely no"
        case 1:
            return "Mostly no"
        case 2:
            return "Undecided"
        case 3:
            return "Mostly yes"
        case 4:
            return "Definitely yes"
    }
}

function load_cur_img() {
    // just an easy way to refer to this
    const data = globalThis.data
    const data_i = globalThis.data_i

    $("#progress").html(`
        <strong>Progress:</strong> ${data_i + 1}/${data.length},
        <strong>UID:</strong> ${globalThis.uid},
        <strong>img:</strong> ${data[data_i]["img"]}
    `)
    $("#prompt").text(data[data_i]["prompt"])

    $("#generated_img").html("<img src='" + IMGDATA_ROOT + data[data_i]["img"] + "'>")

    an_area_var.html("")
    data[data_i]["questions"].forEach((question: string, question_i: number) => {
        let new_an = $(`
            <div>
                <span>${question}</span>
                <span id="q_${question_i}_val" class="slider_val">-</span>
                <input id="q_${question_i}" type="range" min="0" max="4" step="1">
            </div>
        `)
        an_area_var.append(new_an);
        bind_labels(question_i);
    })


    if (!data[data_i].hasOwnProperty("response")) {
        data[data_i]["response"] = []
        data[data_i]["questions"].forEach((question: string) => {
            // set default response
            data[data_i]["response"].push(-1);
        });

        // space for comments
        data[data_i]["response"].push("")
    }

    // resets values
    data[data_i]["questions"].forEach((question: string, question_i: number) => {
        $("#q_" + question_i.toString()).val(data[data_i]["response"][question_i]);
        $("#q_" + question_i.toString() + "_val").text(num_to_answer(data[data_i]["response"][question_i]));
    })

    $("#q_comment").val(data[data_i]["response"][data[data_i]["response"].length - 1])

}

function bind_labels(question_i: number) {
    $("#q_" + question_i.toString()).on('input change', function () {
        let val = parseInt($(this).val() as string);
        globalThis.data[globalThis.data_i]["response"][question_i] = val;

        let slider_obj_val = $("#q_" + question_i.toString() + "_val");
        slider_obj_val.text(num_to_answer(val))
    });

    // special handling of default "empty" value
    $("#q_" + question_i.toString()).on('click', function () {
        if (globalThis.data[globalThis.data_i]["response"][question_i] == -1) {
            globalThis.data[globalThis.data_i]["response"][question_i] = 0;

            let val = parseInt($(this).val() as string);
            console.log(val)
            let slider_obj_val = $("#q_" + question_i.toString() + "_val");
            slider_obj_val.text(num_to_answer(val))
        }
    });
}

function setup() {
    $("#q_comment").on("input change", function () {
        let val = $(this).val() as string
        // set the last response to comment
        let data_cur = globalThis.data[globalThis.data_i]
        globalThis.data[globalThis.data_i]["response"][data_cur["response"].length - 1] = val
    })

    // send current data
    // load next image
    $("#an_next").on("click", () => {
        globalThis.data_i += 1;
        if (globalThis.data_i >= globalThis.data.length) {
            alert("You completed the whole queue, thanks! Wait a few seconds to finish synchronization.");
            globalThis.data_i = 0;
        }

        log_data()
        load_cur_img()
    })

    $("#an_prev").on("click", () => {
        globalThis.data_i -= 1;
        // modulo
        if (globalThis.data_i < 0) {
            globalThis.data_i = globalThis.data.length - 1;
        }

        log_data()
        load_cur_img()
    })
}


export { setup, load_cur_img }