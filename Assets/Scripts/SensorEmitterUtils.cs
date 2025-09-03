using UnityEngine;
using Vector3 = UnityEngine.Vector3;
using System.Collections.Generic;

using BertisUtils;

namespace ExplodotechUtils
{
    public enum EM_Spectrum
    {
        LowFreq,
        Radio,
        MicroWave,
        TeraHertz,
        Infrared,
        VisibleLight,
        UltraViolett,
        XRay,
        GammaRay,
        CosmicRay
    }

    [System.Serializable]
    public class BandData
    {
        /*
        * A datapoint signifing the stremgth of a particular band from the spectrum.
        */
        public string emissionType;
        public float strength;
    }

    [System.Serializable]
    public class SpectrumProfile
    {
        public List<BandData> spectrum;
    }

    public class SensorUtils
    {
        public static (Vector3[], Vector2[]) CalculateCone(Vector3 origin, float directionAngle, float fov, int rayCount, float sensorRange)
        {
            float angle = directionAngle;
            float angleIncrement = fov / rayCount;

            Vector3[] result3 = new Vector3[rayCount + 1 + 1];
            Vector2[] result2 = new Vector2[result3.Length];

            result3[0] = origin;
            result2[0] = result3[0];
            int vertexIndex = 1;

            for (int i = 0; i <= rayCount; i++)
            {

                Vector3 vertex = origin + VectorUtils.GetVectorFromAngle(angle) * sensorRange;
                result3[vertexIndex] = vertex;
                result2[vertexIndex] = vertex;

                vertexIndex++;
                angle -= angleIncrement;

            }


            return (result3, result2);
        }

        public static void SetObjectVisible(GameObject obj, bool visible)
        {

            /*
            * For the time being visibility is just a question of setting the z-Position of an object.
            */

            float newZ = 0f;
            // Create a new Vector3 with the updated z-position and the old x and y.
            if (visible)
            {
                newZ = 1f;
            }

            VectorUtils.TransformSetZ(obj, newZ);

        }

    }

}