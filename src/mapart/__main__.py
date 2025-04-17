

### MATLAB SRC to adapt
for r = 1:(dims(1) - 1) % Last row is padding
    for c = 2:(dims(2) - 1) % First and last columns are padding
        % For each pixel:
        for color = 1:153
            % Calculate errors in luma and chroma for each map color
            % Checks every color, probably not optimized
            for n = 1:3
                diff(n) = image(r, c, n) - palette(color, n + 1);
            end
            diff(1) = lumaWeight*diff(1); % Increase weight on luma
            currentPx(color) = dot(diff, diff);
            % Square and sum component errors
        end
        [~, best] = min(currentPx); % Pick best color, store index
        for n = 1:3
            % Update output matrix
            mapArt(r, c, n) = palette(best, n + 1);
            ID(r, c) = palette(best, 1);
            % Diffuse errors with Floyd-Steinberg dithering
            % Parameter fsDith changes weight of dither to avoid
            % uncontrollable propagation of error
            error(n) = fsDith*(image(r, c, n) - mapArt(r, c, n));
            image(r    , c + 1, n) = image(r    , c + 1, n) + 7/16*error(n);
            image(r + 1, c - 1, n) = image(r + 1, c - 1, n) + 3/16*error(n);
            image(r + 1, c    , n) = image(r + 1, c    , n) + 5/16*error(n);
            image(r + 1, c + 1, n) = image(r + 1, c + 1, n) + 1/16*error(n);
        end
    end
end

### MATLAB SRC for chroma and luma conversion
function [imageLC] = RGB2LC(imageRGB)
% Changes the RGB values of an image into brightness and two color components
dims = size(imageRGB);
imageLC = zeros(dims);
imageRGB = double(imageRGB);
matrix = [0.2126 0.7152 0.0722; 1 -0.5 -0.5; 0 sqrt(3)/2 -sqrt(3)/2];
for r = 1:dims(1)
    for c = 1:dims(2)
        pixel = [imageRGB(r, c, 1); imageRGB(r, c, 2); imageRGB(r, c, 3)];
        pixel = matrix*pixel;
        for n = 1:3
            imageLC(r, c, n) = pixel(n);
        end
    end
end
imageLC = double(imageLC);
end


function [imageRGB] = LC2RGB(imageLC)
% Changes image parameters from brightness and two colors 
dims = size(imageLC);
imageRGB = zeros(dims);
imageLC = double(imageLC);
matrix = [0.2126 0.7152 0.0722; 1 -0.5 -0.5; 0 sqrt(3)/2 -sqrt(3)/2];
for r = 1:dims(1)
    for c = 1:dims(2)
        pixel = [imageLC(r, c, 1); imageLC(r, c, 2); imageLC(r, c, 3)];
        pixel = matrix\pixel;
        for n = 1:3
            imageRGB(r, c, n) = pixel(n);
        end
    end
end
imageRGB = double(imageRGB);
end
