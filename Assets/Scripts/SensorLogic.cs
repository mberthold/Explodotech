using UnityEngine;
using Vector3 = UnityEngine.Vector3;
using BertisUtils;
using Unity.VisualScripting;
using UnityEngine.Rendering;
using System.Collections.Generic;

namespace ExplodotechUtils
{
    public class SensorGeneric
    {
        protected Vector3 position;

        // This List is populated in Sensor.cs using Unity specific methods! We do not care how it was populated!!
        public List<GameObject> ObjectsInCone = new List<GameObject>();
        public List<GameObject> DetectedObjects = new List<GameObject>();
        private SpectrumProfile detectionProfile;
        public Dictionary<EM_Spectrum, float> detectionProfileDict = new Dictionary<EM_Spectrum, float>();

        public SensorGeneric(SpectrumProfile profile)
        {
            this.detectionProfile = profile;
            // Populate the dictionary from the deserialized data.
            foreach (var data in profile.spectrum)
            {
                // Parse the string from the JSON file back into the enum.
                EM_Spectrum type = (EM_Spectrum)System.Enum.Parse(typeof(EM_Spectrum), data.emissionType);
                detectionProfileDict.Add(type, data.strength);
            }
        }

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

        public SensorPassive(SpectrumProfile profile) : base(profile)
        {

        }

        protected override bool DetectObject(GameObject obj)
        {

            Emitter emitter = obj.GetComponentInChildren<Emitter>();
            float distance = Vector3.Distance(obj.transform.position, this.position);
            //Debug.Log("Distance: " + distance);
            float totalOverlapScore = 0f;

            if (emitter == null) return false; // If there is no emitter we can stop this whole thing and return false!

            Dictionary<EM_Spectrum, float> emissionProfile = emitter.GetEmissionProfile();
            foreach (var item in detectionProfileDict)
            {
                if (emissionProfile.ContainsKey(item.Key))
                {
                    float emitterValue = emissionProfile[item.Key];
                    float sensorValue = item.Value;

                    // Multiply the sensor's value by the emitter's value and add to the total.
                    totalOverlapScore += emitterValue * sensorValue;
                } 
            }

            // Emitter's strength (not adjusted!)
            float strength = emitter.signalStrength;
            // Received signal strength - adjusted for distance!
            totalOverlapScore = totalOverlapScore / (distance * distance);
            //Debug.Log("Received signal: " + totalOverlapScore);

            if (totalOverlapScore >= SignalThreshold)
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