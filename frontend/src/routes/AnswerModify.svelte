<script>
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import Error from "../componets/Error.svelte";

    export let params = {};
    const answer_id = params.answer_id;

    let error = { detail: [] };
    let question_id = 0;
    let content = "";

    fastapi("get", "/api/answer/detail/" + answer_id, {}, (json) => {
        question_id = json.question_id;
        content = json.content;
    });

    function update_answer(event) {
        event.preventDefault();
        let url = "/api/answer/update";
        let params = {
            answer_id: answer_id,
            content: content,
        };
        fastapi(
            "put",
            url,
            params,
            (json) => {
                push("/detail/" + question_id);
            },
            (json_error) => {
                error = json_error;
            },
        );
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Edit answer</h5>
    <Error {error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">Content</label>
            <textarea class="form-control" rows="10" bind:value={content}
            ></textarea>
        </div>
        <button class="btn btn-primary" on:click={update_answer}>Update</button>
    </form>
</div>
