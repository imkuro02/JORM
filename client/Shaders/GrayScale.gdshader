shader_type canvas_item;
uniform sampler2D SCREEN_TEXTURE : hint_screen_texture, filter_linear_mipmap;
uniform float intensity : hint_range(0.0, 1.0) = 1.0;

void fragment() {
    vec4 color = texture(SCREEN_TEXTURE, SCREEN_UV);
    
    // Calculate the grayscale value using the luminance formula
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    
    // Mix the original color with the grayscale color based on the intensity
    color.rgb = mix(color.rgb, vec3(gray), intensity);
    
    // Set the output color
    COLOR = color;
}
