#include <SDL.h>
#include <SDL_ttf.h>
#include <iostream>
#include <string>
#include <sstream>
#include <cstdlib>

template <typename T>
std::string to_string(const T& value) {
    std::ostringstream oss;
    oss << value;
    return oss.str();
}

void cleanUp(SDL_Window* window, SDL_Renderer* renderer, TTF_Font* wave_font, TTF_Font* score_font) {
    if (wave_font) TTF_CloseFont(wave_font);
    if (score_font) TTF_CloseFont(score_font);
    if (renderer) SDL_DestroyRenderer(renderer);
    if (window) SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();
}

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "SDL_Init Error: " << SDL_GetError() << std::endl;
        return -1;
    }

    if (TTF_Init() == -1) {
        std::cerr << "TTF_Init Error: " << TTF_GetError() << std::endl;
        SDL_Quit();
        return -1;
    }

    SDL_Window* window = SDL_CreateWindow("ThePOCGame", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 480, 640, 0);
    if (!window) {
        std::cerr << "SDL_CreateWindow Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return -1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "SDL_CreateRenderer Error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_Quit();
        return -1;
    }

    TTF_Font* wave_font = TTF_OpenFont("Consolas.ttf", 30);
    TTF_Font* score_font = TTF_OpenFont("Consolas.ttf", 20);
    if (!wave_font || !score_font) {
        std::cerr << "TTF_OpenFont Error: " << TTF_GetError() << std::endl;
        cleanUp(window, renderer, wave_font, score_font);
        return -1;
    }

    SDL_Event event;
    SDL_Rect Player_rect = { 30, 320, 45, 60 };
    SDL_Rect pipe_rect = { 480, 320, 45, 70 };

    int score = 0;
    int pipe_speed = 5;
    std::string wave_text = "Wave 1";
    float Player_velocity = 0;
    float gravity = 0.75f;
    float jump_strength = -12.0f;

    bool running = true;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
            if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_SPACE) {
                Player_velocity = jump_strength;
            }
        }

        // Apply gravity
        Player_velocity += gravity;
        if (Player_velocity > 50.0f) Player_velocity = 50.0f;
        Player_rect.y += static_cast<int>(Player_velocity);

        // Wrap the player around the screen
        if (Player_rect.y > 640) Player_rect.y = 0;
        if (Player_rect.y < 0) Player_rect.y = 640;

        // Move the pipe and reset its position if it goes off-screen
        pipe_rect.x -= pipe_speed;
        if (pipe_rect.x < -pipe_rect.w) {
            pipe_rect.x = 480;
            pipe_rect.y = rand() % 570;
            score++;
        }

        // Adjust game difficulty based on score
        if (score <= 10) {
            pipe_speed = 5;
            wave_text = "Wave 1";
        }
        else if (score <= 20) {
            pipe_speed = 10;
            wave_text = "Wave 2";
        }
        else if (score <= 30) {
            pipe_speed = 15;
            wave_text = "Wave 3";
        }
        else if (score <= 40) {
            pipe_speed = 20;
            wave_text = "Wave 4";
        }
        else if (score <= 50) {
            pipe_speed = 25;
            wave_text = "Wave 5";
        }

        // Check for collision
        if (SDL_HasIntersection(&Player_rect, &pipe_rect)) {
            score = 0; // Reset score on collision
        }

        // Render everything
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Black background
        SDL_RenderClear(renderer);

        // Render the player
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Red for the player
        SDL_RenderFillRect(renderer, &Player_rect);

        // Render the pipe
        SDL_SetRenderDrawColor(renderer, 255, 255, 0, 255); // Yellow for the pipe
        SDL_RenderFillRect(renderer, &pipe_rect);

        // Render wave text
        SDL_Surface* wave_surface = TTF_RenderText_Solid(wave_font, wave_text.c_str(), { 255, 255, 255 });
        SDL_Texture* wave_texture = SDL_CreateTextureFromSurface(renderer, wave_surface);
        SDL_Rect wave_rect = { 135, 600, wave_surface->w, wave_surface->h };
        SDL_RenderCopy(renderer, wave_texture, nullptr, &wave_rect);
        SDL_FreeSurface(wave_surface);
        SDL_DestroyTexture(wave_texture);

        // Render score
        std::string score_text = "Score: " + to_string(score);
        SDL_Surface* score_surface = TTF_RenderText_Solid(score_font, score_text.c_str(), { 255, 255, 255 });
        SDL_Texture* score_texture = SDL_CreateTextureFromSurface(renderer, score_surface);
        SDL_Rect score_rect = { 0, 0, score_surface->w, score_surface->h };
        SDL_RenderCopy(renderer, score_texture, nullptr, &score_rect);
        SDL_FreeSurface(score_surface);
        SDL_DestroyTexture(score_texture);

        SDL_RenderPresent(renderer);
        SDL_Delay(1000 / 60); // Cap frame rate to ~60 FPS
    }

    cleanUp(window, renderer, wave_font, score_font);
    return 0;
}
