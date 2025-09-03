using UnityEngine;
using Vector3 = UnityEngine.Vector3;
using System.Collections.Generic;

using BertisUtils;

namespace ExplodotechUtils
{
    public class EmitterGeneric
    {
        public Dictionary<EM_Spectrum, float> emissionProfileDict = new Dictionary<EM_Spectrum, float>();
        public SpectrumProfile emissionProfileProf;

        public EmitterGeneric(SpectrumProfile profile)
        {
            this.emissionProfileProf = profile;
            // Populate the dictionary from the deserialized data.
            foreach (var data in profile.spectrum)
            {
                // Parse the string from the JSON file back into the enum.
                EM_Spectrum type = (EM_Spectrum)System.Enum.Parse(typeof(EM_Spectrum), data.emissionType);
                emissionProfileDict.Add(type, data.strength);
            }
        }

        public Dictionary<EM_Spectrum, float> GetEmissionProfile()
        {
            return emissionProfileDict;
        }

    }
}