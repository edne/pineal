#include <SFML/Graphics.hpp>
#include <signals.hpp>

class Entity {
    public:
        void attribute(std::string key, Signal s);
        void apply_all_attributes();
        virtual void apply_attribute(std::string key, Signal s) {};
        virtual ~Entity() {};

    protected:
        std::map<std::string, Signal> attributes;
};

class Drawable : public Entity {
    public:
        virtual void draw(sf::RenderTarget* target, sf::RenderStates states) {};
        virtual ~Drawable() {};
};

class Group : public Drawable {
    public:
        Group() : depth(1) {};
        Group(std::string name);

        void add(Drawable* d);
        virtual void apply_attribute(std::string key, Signal s);
        virtual void draw(sf::RenderTarget* target, sf::RenderStates states);

    protected:
        std::vector<Drawable*> elements;
        sf::Transform sf_transform;
        int depth;
};

class Polygon : public Drawable {
    public:
        Polygon(int);

        void apply_attribute(std::string key, Signal s);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    protected:
        sf::CircleShape sf_shape;
};

class Layer : public Drawable {
    public:
        Layer();
        Layer(std::string name);
        static Layer* memo(std::string name);

        void render(Drawable* child);
        void apply_attribute(std::string key, Signal s);
        void draw(sf::RenderTarget* target, sf::RenderStates states);

    private:
        sf::ConvexShape sf_shape;
        sf::RenderTexture render_texture;
        double w, h;
};

class Window : public Entity {
    public:
        Window(std::string name);
        static Window* memo(std::string name);

        void render(Drawable* child);
        bool is_open();

    private:
        sf::RenderWindow render_window;
};
