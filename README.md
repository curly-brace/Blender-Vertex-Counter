# Blender-Vertex-Counter
![alt tag](https://raw.githubusercontent.com/curly-brace/Blender-Vertex-Counter/master/Screenshot_20160814_144740.png)

####Addon to display real vertex count for models that will be used in games

Displays actual vertex count that will be used to render object by game engine, depending on normal smoothing, because game engine will split verticies that have hard edge between them.

Takes into account uv-seams too, because smoothed verticies, that have seam, will be splited.

~~It lags as hell on complex meshes, so there is now option do disable calcs.~~
Updates now happen in at max 1 second intervals. And if you see that blender freezes once a second, just switch off automatic updates and press 'Update' button when you need.

####NOTE FOR FBX EXPORT:
Blender default exporter seems to switch full smooth shading and enable autosmooth for mesh, when default export option for smoothing - 'Normals Only' is active. The mesh appears to have less verts, because of full smooth shading, but the counter of my addon would show wrong vertex number, because mesh was modified outside of blender's 3D View and original mesh remains unchanged.

So it is a good idea to enable smooth shading and autosmooth for the object manualy, so that the counter shows right vertex number. Seems like 50 degrees for angle property shows good results and vertex count. We are creating game models right? They will be heavily textured anyway!

####What does not work:
The calculation will fail in situations when hard edge crosses uv-seam.

See this my question for details and sample.

http://blender.stackexchange.com/questions/60914/how-to-determine-right-vertex-count-for-mesh

For now I have no idea how to fix it.. So beware!
