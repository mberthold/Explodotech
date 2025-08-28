using UnityEngine;
using Vector3 = UnityEngine.Vector3;
using BertisUtils;
using Unity.VisualScripting;
using UnityEngine.Rendering;
using System.Collections.Generic;

namespace ExplodotechUtils
{

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

    public class SensorGeneric
    {
        protected Vector3 position;

        // This List is populated in Sensor.cs using Unity specific methods! We do not care how it was populated!!
        public List<GameObject> ObjectsInCone = new List<GameObject>();
        public List<GameObject> DetectedObjects = new List<GameObject>();

        protected virtual bool DetectObject(GameObject obj)
        {
            /*
            * Take a GameObject (from the List of Objects in the cone) and decide whether or not this Object can be detected by the sensor.
            */
            Emitter emitter = obj.GetComponentInChildren<Emitter>();
            if (emitter != null)
            {
                return true;
            }
            return false;
        }

        public void Scan()
        {
            /*
            * Update the DetectedObjects List.
            * Remove objects that are either not in the cone anymore or cannot be detected anymore.
            * Add newly deteced Objects from the Objects inside the cone!
            */

            // Add new objects
            foreach (GameObject obj in ObjectsInCone)
            {
                if (DetectObject(obj) & !DetectedObjects.Contains(obj)) // If the object is detected but not already in the DetectedObjects list
                {
                    DetectedObjects.Add(obj);
                }

            }

            // Remove objects that are no longer detected!
            for (int i = DetectedObjects.Count - 1; i >= 0; i--)
            {
                GameObject obj = DetectedObjects[i];
                if (!ObjectsInCone.Contains(obj) | !DetectObject(obj))
                {
                    DetectedObjects.RemoveAt(i);
                }
            }
        }

        public void UpdatePosition(Vector3 position)
        {
            this.position = position;
        }
    }

    public class SensorPassive : SensorGeneric
        {
            /*
            * This is a passive Sensor. It does not send out a signal of its own.
            * It only looks and receives signals. Real world example: Mk1 Eyeball!
            * The sensor has a signal threshold above which it detects a signal. 
            * If the signal is below the threshold the sensor does not detect anyting!
            */

            public float SignalThreshold = 1f;

            protected override bool DetectObject(GameObject obj)
            {

                Emitter emitter = obj.GetComponentInChildren<Emitter>();
                float distance = Vector3.Distance(obj.transform.position, this.position);
                Debug.Log("Distance: " + distance);

                if (emitter == null) return false; // If there is no emitter we can stop this whole thing and return false!

                // Emitter's strength (not adjusted!)
                float strength = emitter.signalStrength;
                // Received signal strength - adjusted for distance!
                strength = emitter.signalStrength / (distance * distance);
                Debug.Log("Received signal: " + strength);

                if (strength >= SignalThreshold)
            {
                return true;
            }
            else
            {
                return false;
            }

            }

        }

}