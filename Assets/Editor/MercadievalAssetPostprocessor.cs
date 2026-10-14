// Mercadieval - importacion automatica de assets 2D (Unity 6.3 LTS).
// Aplica el apartado 3.3 de la guia v1.1 (estandar de 64 px: PPU 64, Point, sin compresion, Full Rect, sin mipmaps, Clamp, Alpha Is Transparency)
// y corta las hojas de sprites por tamano de celda segun la carpeta/nombre del archivo.
// Requiere el paquete "2D Sprite" (viene con la plantilla 2D). Menu: Mercadieval > Reimportar assets de arte.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.U2D.Sprites;
using UnityEngine;

namespace Mercadieval.EditorTools
{
    public class MercadievalAssetPostprocessor : AssetPostprocessor
    {
        const string ArtRoot = "Assets/Art/";
        const string AudioRoot = "Assets/Audio/";
        const string Version = "mdv2";

        struct Plan
        {
            public int ppu;
            public int cell;            // 0 = Single
            public SpriteAlignment align;
            public bool panel;          // paneles 1920x1080: compresion normal
            public Vector4 border;      // 9-slice (izq, abajo, der, arriba)
        }

        static Plan PlanFor(string path, int w, int h)
        {
            string p = path.Substring(ArtRoot.Length);
            string n = Path.GetFileNameWithoutExtension(path);
            var plan = new Plan { ppu = 64, cell = 0, align = SpriteAlignment.Center };

            if (p.StartsWith("Characters/"))
            {
                plan.cell = h;                                   // una fila por animacion: celda = alto
                plan.align = n.Contains("candil") ? SpriteAlignment.Center : SpriteAlignment.BottomCenter;
            }
            else if (p.StartsWith("Tilesets/")) { plan.cell = 64; }
            else if (p.StartsWith("Objects/"))
            {
                plan.align = SpriteAlignment.BottomCenter;
                plan.cell = (w == h) ? 0 : h;
            }
            else if (p.StartsWith("Items/")) { plan.cell = p.Contains("singles/") ? 0 : 64; }
            else if (p.StartsWith("UI/Icons/")) { plan.ppu = 128; plan.cell = p.Contains("singles/") ? 0 : 128; }
            else if (p.StartsWith("UI/Elements/"))
            {
                if (n.Contains("marco_ventana")) plan.border = new Vector4(64, 64, 64, 64);
                else if (n.Contains("caja_dialogo") || n.Contains("ventana_comercio") || n.Contains("notificacion")) plan.border = new Vector4(32, 32, 32, 32);
                else if (n.Contains("boton") || n.Contains("pestana")) plan.border = new Vector4(32, 32, 32, 32);
            }
            else if (p.StartsWith("Cinematics/") || p.StartsWith("Screens/")) { plan.panel = true; }
            else if (p.StartsWith("VFX/")) { plan.cell = (w == h) ? 0 : h; }
            return plan;
        }

        static bool ReadPngSize(string assetPath, out int w, out int h)
        {
            w = h = 0;
            try
            {
                using (var fs = File.OpenRead(assetPath))
                {
                    var b = new byte[24];
                    if (fs.Read(b, 0, 24) < 24) return false;
                    w = (b[16] << 24) | (b[17] << 16) | (b[18] << 8) | b[19];
                    h = (b[20] << 24) | (b[21] << 16) | (b[22] << 8) | b[23];
                    return true;
                }
            }
            catch { return false; }
        }

        // ---------------------------------------------------------------- Texturas
        void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith(ArtRoot) || !assetPath.EndsWith(".png")) return;
            if (!ReadPngSize(assetPath, out int w, out int h)) return;
            var plan = PlanFor(assetPath, w, h);
            var ti = (TextureImporter)assetImporter;

            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = plan.cell == 0 ? SpriteImportMode.Single : SpriteImportMode.Multiple;
            ti.spritePixelsPerUnit = plan.ppu;
            ti.filterMode = FilterMode.Point;
            ti.mipmapEnabled = false;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.alphaIsTransparency = true;
            ti.maxTextureSize = 2048;
            ti.textureCompression = plan.panel ? TextureImporterCompression.Compressed : TextureImporterCompression.Uncompressed;
            ti.compressionQuality = 50;

            var s = new TextureImporterSettings();
            ti.ReadTextureSettings(s);
            s.spriteMeshType = SpriteMeshType.FullRect;
            if (plan.cell == 0)
            {
                s.spriteAlignment = (int)plan.align;
                s.spritePivot = PivotOf(plan.align);
                ti.spriteBorder = plan.border;
            }
            ti.SetTextureSettings(s);
        }

        static Vector2 PivotOf(SpriteAlignment a)
        {
            return a == SpriteAlignment.BottomCenter ? new Vector2(0.5f, 0f) : new Vector2(0.5f, 0.5f);
        }

        // Corte de hojas (Grid By Cell Size) una sola vez por archivo.
        static void OnPostprocessAllAssets(string[] imported, string[] deleted, string[] moved, string[] movedFrom)
        {
            foreach (var path in imported)
            {
                if (!path.StartsWith(ArtRoot) || !path.EndsWith(".png")) continue;
                var ti = AssetImporter.GetAtPath(path) as TextureImporter;
                if (ti == null || ti.userData == Version) continue;
                if (!ReadPngSize(path, out int w, out int h)) continue;
                var plan = PlanFor(path, w, h);
                if (plan.cell == 0) { ti.userData = Version; ti.SaveAndReimport(); continue; }
                SliceGrid(ti, w, h, plan);
            }
        }

        static void SliceGrid(TextureImporter ti, int w, int h, Plan plan)
        {
            string name = Path.GetFileNameWithoutExtension(ti.assetPath);
            int cw = plan.cell, ch = plan.cell;
            bool strip = ti.assetPath.Contains("/Characters/") || ti.assetPath.Contains("/Objects/") || ti.assetPath.Contains("/VFX/");
            if (strip) ch = h;   // tiras de animacion: una sola fila
            int cols = w / cw, rows = Mathf.Max(1, h / ch);
            var factory = new SpriteDataProviderFactories();
            factory.Init();
            var dp = factory.GetSpriteEditorDataProviderFromObject(ti);
            dp.InitSpriteEditorDataProvider();

            var rects = new List<SpriteRect>();
            var pairs = new List<SpriteNameFileIdPair>();
            int idx = 0;
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                {
                    var sr = new SpriteRect
                    {
                        name = $"{name}_{idx}",
                        rect = new Rect(c * cw, h - (r + 1) * ch, cw, ch),
                        alignment = plan.align,
                        pivot = PivotOf(plan.align),
                        spriteID = GUID.Generate()
                    };
                    rects.Add(sr);
                    pairs.Add(new SpriteNameFileIdPair(sr.name, sr.spriteID));
                    idx++;
                }
            dp.SetSpriteRects(rects.ToArray());
            var nameProvider = dp.GetDataProvider<ISpriteNameFileIdDataProvider>();
            if (nameProvider != null) nameProvider.SetNameFileIdPairs(pairs);
            dp.Apply();
            ti.userData = Version;
            ti.SaveAndReimport();
        }

        // ---------------------------------------------------------------- Audio
        void OnPreprocessAudio()
        {
            if (!assetPath.StartsWith(AudioRoot)) return;
            var ai = (AudioImporter)assetImporter;
            var set = ai.defaultSampleSettings;
            if (assetPath.Contains("/Music/"))
            {
                set.loadType = AudioClipLoadType.Streaming;
                set.compressionFormat = AudioCompressionFormat.Vorbis;
                set.quality = 0.6f;
                set.preloadAudioData = false;
            }
            else
            {
                set.loadType = AudioClipLoadType.DecompressOnLoad;
                set.compressionFormat = AudioCompressionFormat.PCM;
                set.preloadAudioData = true;
            }
            ai.defaultSampleSettings = set;
            ai.forceToMono = assetPath.Contains("/SFX/");
        }

        [MenuItem("Mercadieval/Reimportar assets de arte")]
        static void ReimportAll()
        {
            foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/Art" }))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                var ti = AssetImporter.GetAtPath(path) as TextureImporter;
                if (ti == null) continue;
                ti.userData = "";
                ti.SaveAndReimport();
            }
        }
    }
}
