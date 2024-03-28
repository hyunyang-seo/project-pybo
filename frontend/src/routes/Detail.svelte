<script>
    import fastapi from "../lib/api";
    import Error from "../componets/Error.svelte";
    import { link, push } from "svelte-spa-router";
    import { is_login, username } from "../lib/store";
    import { marked } from "marked";
    import moment from "moment/min/moment-with-locales";
    moment.locale("en");

    export let params = {}; // To read the parameter value passed when calling the Detail component
    let question_id = params.question_id;
    let question = { answers: [], voter: [], content: "" };
    let content = "";
    let error = { detail: [] };

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json;
        });
    }

    get_question();

    function post_answer(event) {
        event.preventDefault();
        let url = "/api/answer/create/" + question_id;
        let params = {
            content: content,
        };
        fastapi(
            "post",
            url,
            params,
            (json) => {
                content = "";
                error = { detail: [] };
                get_question();
            },
            (json_error) => {
                error = json_error;
            },
        );
    }

    function delete_question(_question_id) {
        if (window.confirm("Are you sure you want to delete it?")) {
            let url = "/api/question/delete";
            let params = {
                question_id: _question_id,
            };
            fastapi(
                "delete",
                url,
                params,
                (json) => {
                    push("/");
                },
                (json_error) => {
                    error = json_error;
                },
            );
        }
    }

    function delete_answer(answer_id) {
        if (window.confirm("Are you sure you want to delete it?")) {
            let url = "/api/answer/delete";
            let params = {
                answer_id: answer_id,
            };
            fastapi(
                "delete",
                url,
                params,
                (json) => {
                    get_question();
                },
                (json_error) => {
                    error = json_error;
                },
            );
        }
    }

    function vote_question(_question_id) {
        if (window.confirm("Would you really recommend it?")) {
            let url = "/api/question/vote";
            let params = {
                question_id: _question_id,
            };
            fastapi(
                "post",
                url,
                params,
                (json) => {
                    get_question();
                },
                (json_error) => {
                    error = json_error;
                },
            );
        }
    }

    function vote_answer(answer_id) {
        if (window.confirm("Would you really recommend it?")) {
            let url = "/api/answer/vote";
            let params = {
                answer_id: answer_id,
            };
            fastapi(
                "post",
                url,
                params,
                (json) => {
                    get_question();
                },
                (json_error) => {
                    error = json_error;
                },
            );
        }
    }
</script>

<div class="container my-3">
    <!-- Question list -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {@html marked.parse(question.content)}
            </div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date}
                    <div class="badge bg-light text-dark p-2 text-start mx-3">
                        <div class="mb-2">modified at</div>
                        <div>
                            {moment(question.modify_date).format(
                                "YYYY-MM-DD hh:mm:ss A",
                            )}
                        </div>
                    </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">
                        {question.user ? question.user.username : ""}
                    </div>
                    <div>
                        {moment(question.create_date).format(
                            "YYYY-MM-DD hh:mm:ss A",
                        )}
                    </div>
                </div>
            </div>
            <div class="my-3">
                <button
                    class="btn btn-sm btn-outline-secondary"
                    on:click={vote_question(question.id)}
                >
                    Recommend
                    <span class="badge rounded-pill bg-success"
                        >{question.voter.length}</span
                    >
                </button>
                {#if question.user && $username == question.user.username}
                    <a
                        use:link
                        href="/question-modify/{question.id}"
                        class="btn btn-sm btn-outline-secondary">Edit</a
                    >
                    <button
                        class="btn btn-sm btn-outline-secondary"
                        on:click={() => delete_question(question.id)}
                        >Delete</button
                    >
                {/if}
            </div>
        </div>
    </div>

    <button
        class="btn btn-secondary"
        on:click={() => {
            push("/");
        }}>To list</button
    >

    <!-- Answer list -->
    <h5 class="border-bottom my-3 py-2">
        There are {question.answers.length} answers.
    </h5>
    {#each question.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">
                    {answer.content}
                </div>
                <div class="d-flex justify-content-end">
                    {#if answer.modify_date}
                        <div
                            class="badge bg-light text-dark p-2 text-start mx-3"
                        >
                            <div class="mb-2">modified at</div>
                            <div>
                                {moment(answer.modify_date).format(
                                    "YYYY-MM-DD hh:mm:ss A",
                                )}
                            </div>
                        </div>
                    {/if}
                    <div class="badge bg-light text-dark p-2 text-start">
                        <div class="mb-2">
                            {answer.user ? answer.user.username : ""}
                        </div>
                        <div>
                            {moment(question.create_date).format(
                                "YYYY-MM-DD hh:mm:ss A",
                            )}
                        </div>
                    </div>
                </div>
                <div class="my-3">
                    <button
                        class="btn btn-sm btn-outline-secondary"
                        on:click={vote_answer(answer.id)}
                    >
                        Recommend
                        <span class="badge rounded-pill bg-success"
                            >{answer.voter.length}</span
                        >
                    </button>
                    {#if answer.user && $username === answer.user.username}
                        <a
                            use:link
                            href="/answer-modify/{answer.id}"
                            class="btn btn-sm btn-outline-secondary">Edit</a
                        >
                        <button
                            class="btn btn-sm btn-outline-secondary"
                            on:click={() => delete_answer(answer.id)}
                            >Delete</button
                        >
                    {/if}
                </div>
            </div>
        </div>
    {/each}
    <!-- Submit answer -->
    <Error {error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea
                rows="10"
                bind:value={content}
                disabled={$is_login ? "" : "disabled"}
                class="form-control"
            />
        </div>
        <input
            type="submit"
            value="Submit answer"
            class="btn btn-primary {$is_login ? '' : 'disabled'}"
            on:click={post_answer}
        />
    </form>
</div>
