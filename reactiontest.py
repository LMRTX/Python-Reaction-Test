import pygame
import time
import random

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

pygame.display.set_caption("ReactionTest")

font = pygame.font.SysFont("JetBrainsMono Nerd Font", 48)
subfont = pygame.font.SysFont("JetBrainsMono Nerd Font", 25)

starttext = font.render("Click To Start", True, (255, 255, 255))
wait_text = font.render("Wait for Green", True, (255, 255, 255))
click_text = font.render("Click!", True, (255, 255, 255))
false_start_text = font.render("Too Soon!", True, (255, 255, 255))
try_again_text = subfont.render("click to try again", True, (255, 255, 255))
tab_bind_text = subfont.render("Tab: Stats", True, (255, 255, 255))
no_runs_text = font.render("No Runs Completed :(", True, (255, 255, 255))
force_restart_text = subfont.render("R: Restart |", True, (255, 255, 255))

clock = pygame.time.Clock()

width, height = window.get_size()

running = True
begin = True
clicked = False
started = False
waiting = False
false_start = False
restart = False
stat_page = False
force_restart = False


target = 0
wait_time = 0

totalruns = 0
totalms = 0

run_count = 0
session_total_ms = 0
session_complete = False

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = pygame.display.get_surface()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if stat_page:
                continue

            elif false_start:
                false_start = False
                begin = False
                started = True
                wait_time = time.perf_counter() + random.uniform(1.5, 3.0)

            elif started:
                started = False
                false_start = True
                waiting = False
                clicked = False

            elif begin:
                begin = False
                started = True
                wait_time = time.perf_counter() + random.uniform(1.5, 3.0)

            elif waiting:
                clicked = True
                waiting = False

                elapsed_ms = round((time.perf_counter() - target) * 1000)

                run_count += 1
                totalruns += 1
                totalms += elapsed_ms
                session_total_ms += elapsed_ms

                if run_count == 5:
                    resulttext = font.render(
                        f"Average: {round(session_total_ms / 5)}ms",
                        True, (255, 255, 255)
                    )
                    session_complete = True

                else:
                    resulttext = font.render(
                        f"{elapsed_ms}ms ({run_count}/5)",
                        True, (255, 255, 255)
                    )
                    session_complete = False

            elif restart:
                restart = False
                clicked = False

                if session_complete:
                    run_count = 0
                    session_total_ms = 0
                    session_complete = False
                    begin = True
                else:
                    begin = False
                    started = True
                    wait_time = time.perf_counter() + random.uniform(1.5, 3.0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if not stat_page:
                    stat_page = True
                    waiting = False
                    begin = False
                    started = False
                    clicked = False
                    restart = False

                else:
                    stat_page = False

                    if session_complete:
                        begin = False
                        clicked = True
                        restart = True
                    elif run_count > 0:
                        begin = False
                        clicked = True
                        restart = True
                    else:
                        begin = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                false_start = False
                waiting = False
                begin = False
                started = False
                clicked = False
                restart = False
                force_restart = True

    if started and time.perf_counter() >= wait_time:
        started = False
        waiting = True
        target = time.perf_counter()

    clock.tick(360)

    if force_restart:
        restart = False
        clicked = False
        false_start = False
        waiting = False
        begin = True
        started = False

        run_count = 0
        session_total_ms = 0
        session_complete = False

        force_restart = False

    if stat_page:
        window.fill((0, 0, 0))

        if totalruns <= 0:
            window.blit(no_runs_text, (
                width // 2 - no_runs_text.get_width() / 2,
                height // 2 - no_runs_text.get_height() / 2
            ))

        if totalruns == 1:
            totalruns_text = font.render(
                f"You have completed {totalruns} run",
                True, (255, 255, 255)
            )
            window.blit(totalruns_text, (
                width // 2 - totalruns_text.get_width() // 2,
                height // 2 - totalruns_text.get_height() // 2
            ))

            average_text = font.render(
                f"Your average is {round(totalms / totalruns)}ms",
                True, (255, 255, 255)
            )
            window.blit(average_text, (
                width // 2 - average_text.get_width() // 2,
                height // 2 - average_text.get_height() // 2
                - totalruns_text.get_height()
            ))

        if totalruns > 1:
            totalruns_text = font.render(
                f"You have completed {totalruns} runs",
                True, (255, 255, 255)
            )
            window.blit(totalruns_text, (
                width // 2 - totalruns_text.get_width() // 2,
                height // 2 - totalruns_text.get_height() // 2
            ))

            average_text = font.render(
                f"Your average is {round(totalms / totalruns)}ms",
                True, (255, 255, 255)
            )
            window.blit(average_text, (
                width // 2 - average_text.get_width() // 2,
                height // 2 - average_text.get_height() // 2
                - totalruns_text.get_height()
            ))

    if false_start:
        window.fill((0, 0, 0))

        window.blit(false_start_text, (
            width / 2 - false_start_text.get_width() / 2,
            height / 2 - false_start_text.get_height() / 2
        ))

        window.blit(try_again_text, (
            width / 2 - try_again_text.get_width() / 2,
            height / 2 - try_again_text.get_height() / 2
            + false_start_text.get_height()
        ))

    elif begin:
        window.fill((0, 0, 0))

        window.blit(starttext, (
            width / 2 - starttext.get_width() / 2,
            height / 2 - starttext.get_height() / 2
        ))

        window.blit(tab_bind_text, (
            width - tab_bind_text.get_width() - 5,
            height - tab_bind_text.get_height()
        ))

        window.blit(force_restart_text, (
            width - force_restart_text.get_width() - tab_bind_text.get_width() - 20,
            height - force_restart_text.get_height()
        ))



    elif started:
        window.fill((180, 0, 0))

        window.blit(wait_text, (
            width / 2 - wait_text.get_width() / 2,
            height / 2 - wait_text.get_height() / 2
        ))

    elif waiting:
        window.fill((0, 120, 0))

        window.blit(click_text, (
            width / 2 - click_text.get_width() / 2,
            height / 2 - click_text.get_height() / 2
        ))

    elif clicked:
        window.fill((0, 0, 0))

        window.blit(resulttext, (
            width / 2 - resulttext.get_width() / 2,
            height / 2 - resulttext.get_height() / 2
        ))

        if session_complete:
            completion_text = subfont.render(
                "Session complete! Click to continue",
                True, (255, 255, 255)
            )
            window.blit(tab_bind_text, (
            width - tab_bind_text.get_width() - 5,
            height - tab_bind_text.get_height()
            ))
        else:
            completion_text = subfont.render(
                "Click to continue",
                True, (255, 255, 255)
            )

        window.blit(completion_text, (
            width / 2 - completion_text.get_width() / 2,
            height / 2 + resulttext.get_height()
        ))

        restart = True

    pygame.display.flip()

pygame.quit()


